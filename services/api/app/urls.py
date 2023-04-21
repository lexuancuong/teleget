# from aqi import api as aqi_api
from aqi.views import router as aqi_router
from django.urls import path
from elevation.views import router as elevation_router
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('elevation', elevation_router)
api.add_router('aqi', aqi_router)

urlpatterns = [
    path("api/", api.urls),
]
