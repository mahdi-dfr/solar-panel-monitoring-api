from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    PanelViewSet,
    ProjectWeatherView,
    ConvertCityToLatlongView,
    PanelPowerView,
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("panels", PanelViewSet, basename="panel")

urlpatterns = [
    path("weather/", ProjectWeatherView.as_view(), name="weather"),
    path("latlong/", ConvertCityToLatlongView.as_view(), name="latlong"),
    path("panels/<int:board_id>/power/", PanelPowerView.as_view(), name="panel-power"),
] + router.urls