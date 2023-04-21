FROM osgeo/gdal:ubuntu-full-3.5.2
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        gcc \
        g++ \
        supervisor \
        libmemcached-dev \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*


ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV GDAL_DISABLE_READDIR_ON_OPEN=TRUE
ENV GDAL_NUM_THREADS=ALL_CPUS
ENV GDAL_CACHEMAX=512

RUN pip --no-cache-dir install --upgrade pip==22.1.2
# This one so big, need to re-build the wheel again.
# Put this one here to reduce the build time.
RUN pip install rasterio==1.2.10
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r ./requirements.txt && \
    rm -rf /root/.cache/pip/* && \
    rm ./requirements.txt

RUN mkdir -p /srv/teleget/
WORKDIR /srv/teleget/

ADD . ./
RUN chmod 775 start.sh
ENTRYPOINT ["/srv/teleget/start.sh"]
CMD []
