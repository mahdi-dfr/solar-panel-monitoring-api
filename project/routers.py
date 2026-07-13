from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    ProjectWeatherView,
    ConvertCityToLatlongView,
    ProjectLiveDataAPIView

)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
# router.register("strings_reading", StringReadingViewSet, basename="string_reading")
# router.register("panels", PanelViewSet, basename="panel")

urlpatterns = [
    path("weather/", ProjectWeatherView.as_view(), name="weather"),
    path("latlong/", ConvertCityToLatlongView.as_view(), name="latlong"),
    path(
        'projects/<int:project_id>/live-data/',
        ProjectLiveDataAPIView.as_view(),
        name='project-live-data'
    ),
    # path("panels/<int:board_id>/power/", PanelPowerView.as_view(), name="panel-power"),
] + router.urls