from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import ProjectViewSet, PanelViewSet, ProjectWeatherView, ConvertCityToLatlongView

router = DefaultRouter()
router.register('projects' ,ProjectViewSet, basename='projects')
router.register('panels', PanelViewSet, basename='panel')


urlpatterns = [
    path('weather/', ProjectWeatherView.as_view(), name='weather'),
    path('latlong/', ConvertCityToLatlongView.as_view(), name='latlong'),
] + router.urls