from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import ProjectViewSet, PanelViewSet

router = DefaultRouter()
router.register('projects' ,ProjectViewSet, basename='projects')
router.register('panels', PanelViewSet, basename='panel')
# router.register('weather', WeatherView, basename='Weather')


urlpatterns = [] + router.urls