from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework.views import APIView
from . serializer import ProjectSerializer, PanelSerializer
from . models import Project, Panel
from solar_monitoring_api import settings
import requests

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .models import Project, Panel


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PanelViewSet(ModelViewSet):
    serializer_class = PanelSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')

        if not project_id:
            return Panel.objects.none()

        return Panel.objects.filter(
            project__id=project_id,
            project__user=self.request.user
        )

    def perform_create(self, serializer):
        project_id = self.request.query_params.get('project_id')

        if not project_id:
            raise ValidationError({
                "project_id": "لطفاً project_id را در query params ارسال کنید."
            })

        try:
            project = Project.objects.get(
                id=project_id,
                user=self.request.user
            )
        except Project.DoesNotExist:
            raise ValidationError({
                "project_id": "پروژه‌ای با این شناسه برای این کاربر وجود ندارد."
            })

        serializer.save(project=project)


class WeatherView(APIView):

    def get(self, request):    
        city = request.query_params.get('city')

        url = 'https://api.weatherapi.com/v1/current.json'

        params = {
            "key": settings.WEATHER_API_KEY,
            "q": f'{city},IR'
        }

        print(params)

        try:
        
            response = requests.get(url, params)
            data = response.json()


            return Response({"city": data["location"]["name"],
                "temp_c": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "condition": data["current"]["condition"]["text"],})
        
        except requests.exceptions.Timeout:
            return Response(
                {"error": "Weather service timeout"},
                status=504
            )

        except requests.exceptions.ConnectionError:
            return Response(
                {"error": "Cannot connect to weather service"},
                status=503
            )

        except requests.exceptions.HTTPError as e:
            return Response(
                {"error": "Weather API error", "detail": str(e)},
                status=502
            )
        

