import numpy as np
import pyproj
import rasterio
from django.conf import settings
from rasterio.enums import Resampling

INTERPOLATION_METHODS = {
    "nearest": Resampling.nearest,
    "bilinear": Resampling.bilinear,
    "cubic": Resampling.cubic,
}


def _validate_points_lie_within_raster(xs, ys, lats, lons, bounds, res):
    """Check that querying the dataset won't throw an error.

    Args:
        xs, ys: Lists/arrays of x/y coordinates, in projection of file.
        lats, lons: Lists/arrays of lat/lon coordinates. Only used for error message.
        bounds: rastio BoundingBox object.
        res: Tuple of (x_res, y_res) resolutions.

    Raises:
        ValueError: if one of the points lies outside bounds.
    """
    oob_indices = set()

    # Get actual extent. When storing point data in a pixel-based raster
    # format, the true extent is the centre of the outer pixels, but GDAL
    # reports the extent as the outer edge of the outer pixels. So need to
    # adjust by half the pixel width.
    #
    # Also add an epsilon to account for
    # floating point precision issues: better to validate an invalid point
    # which will error out on the reading anyway, than to invalidate a valid
    # point.
    atol = 1e-8
    x_min = min(bounds.left, bounds.right) + abs(res[0]) / 2 - atol
    x_max = max(bounds.left, bounds.right) - abs(res[0]) / 2 + atol
    y_min = min(bounds.top, bounds.bottom) + abs(res[1]) / 2 - atol
    y_max = max(bounds.top, bounds.bottom) - abs(res[1]) / 2 + atol

    # Check bounds.
    x_in_bounds = (xs >= x_min) & (xs <= x_max)
    y_in_bounds = (ys >= y_min) & (ys <= y_max)

    # Found out of bounds.
    oob_indices.update(np.nonzero(~x_in_bounds)[0])
    oob_indices.update(np.nonzero(~y_in_bounds)[0])
    return sorted(oob_indices)


_TRANSFORMER_CACHE = {}


def reproject_latlons(lats, lons, epsg=None, wkt=None):
    """Convert WGS84 latlons to another projection.

    Args:
        lats, lons: Lists/arrays of latitude/longitude numbers.
        epsg: Integer EPSG code.

    """
    if epsg is None and wkt is None:
        raise ValueError("Must provide either epsg or wkt.")

    if epsg and wkt:
        raise ValueError("Must provide only one of epsg or wkt.")

    if epsg == WGS84_LATLON_EPSG:
        return lons, lats

    # Validate EPSG.
    if epsg is not None and (not 1024 <= epsg <= 32767):
        raise ValueError("Dataset has invalid epsg projection.")

    # Load transformer.
    to_crs = wkt or f"EPSG:{epsg}"
    if to_crs in _TRANSFORMER_CACHE:
        transformer = _TRANSFORMER_CACHE[to_crs]
    else:
        from_crs = f"EPSG:{WGS84_LATLON_EPSG}"
        transformer = pyproj.transformer.Transformer.from_crs(
            from_crs, to_crs, always_xy=True
        )
        _TRANSFORMER_CACHE[to_crs] = transformer

    # Do the transform.
    x, y = transformer.transform(lons, lats)

    return x, y


WGS84_LATLON_EPSG = 4326


def _get_elevation_from_path(
    lats,
    lons,
    path=settings.BASE_DIR / 'data/dem_compress.tif',
    interpolation='bilinear',
):
    """Read values at locations in a raster.

    Args:
        lats, lons: Arrays of latitudes/longitudes.
        path: GDAL supported raster location.
        interpolation: method name string.

    Returns:
        z_all: List of elevations, same length as lats/lons.
    """
    z_all = []
    interpolation = INTERPOLATION_METHODS.get(interpolation)
    lons = np.asarray(lons)
    lats = np.asarray(lats)

    try:
        with rasterio.open(path) as f:
            if f.crs is None:
                msg = "Dataset has no coordinate reference system."
                msg += f" Check the file '{path}' is a geo raster."
                msg += " Otherwise you'll have to add the crs manually with a tool like gdaltranslate."
                raise ValueError(msg)

            try:
                if f.crs.is_epsg_code:
                    xs, ys = reproject_latlons(lats, lons, epsg=f.crs.to_epsg())
                else:
                    xs, ys = reproject_latlons(lats, lons, wkt=f.crs.to_wkt())
            except ValueError:
                raise ValueError("Unable to transform latlons to dataset projection.")

            # Check bounds.
            oob_indices = _validate_points_lie_within_raster(
                xs, ys, lats, lons, f.bounds, f.res
            )
            rows, cols = tuple(f.index(xs, ys, op=lambda x: x))

            # Different versions of rasterio may or may not collapse single
            # f.index() lookups into scalars. We want to always have an
            # array.
            rows = np.atleast_1d(rows)
            cols = np.atleast_1d(cols)

            # Offset by 0.5 to convert from center coords (provided by
            # f.index) to ul coords (expected by f.read).
            rows = rows - 0.5
            cols = cols - 0.5

            # Because of floating point precision, indices may slightly exceed
            # array bounds. Because we've checked the locations are within the
            # file bounds,  it's safe to clip to the array shape.
            rows = rows.clip(0, f.height - 1)
            cols = cols.clip(0, f.width - 1)

            # Read the locations, using a 1x1 window. The `masked` kwarg makes
            # rasterio replace NODATA values with np.nan. The `boundless` kwarg
            # forces the windowed elevation to be a 1x1 array, even when it all
            # values are NODATA.
            for i, (row, col) in enumerate(zip(rows, cols)):
                if i in oob_indices:
                    z_all.append(None)
                    continue
                window = rasterio.windows.Window(col, row, 1, 1)
                z_array = f.read(
                    indexes=1,
                    window=window,
                    resampling=interpolation,
                    out_dtype=float,
                    boundless=True,
                    masked=True,
                )
                z = np.ma.filled(z_array, np.nan)[0][0]
                z_all.append(z)

    # Depending on the file format, when rasterio finds an invalid projection
    # of file, it might load it with a None crs, or it might throw an error.
    except rasterio.RasterioIOError as e:
        if "not recognized as a supported file format" in str(e):
            msg = f"Dataset file '{path}' not recognised as a geo raster."
            msg += " Check that the file has projection information with gdalsrsinfo,"
            msg += " and that the file is not corrupt."
            raise ValueError(msg)
        raise e

    return z_all


def get_single_elevation(lat: float, long: float):
    if res := _get_elevation_from_path([float(lat)], [float(long)]):
        return res[0]
