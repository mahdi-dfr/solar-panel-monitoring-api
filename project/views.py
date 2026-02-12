from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import quote


from rest_framework.views import APIView
from . serializer import ProjectSerializer, PanelSerializer
from . models import Project, Panel
from solar_monitoring_api import settings
import requests

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .models import Project, Panel
from utilities.utility import get_or_fetch_lat_long


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        city = serializer.validated_data.get("city")

        lat = None
        lng = None

        if city:
            try:
                lat, lng = get_or_fetch_lat_long(city)
            except Exception as e:
                raise ValidationError({
                    "city": f"خطا در دریافت مختصات شهر: {str(e)}"
                })

        serializer.save(
            user=self.request.user,
            latitude=lat,
            longitude=lng
        )


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


class ProjectWeatherView(APIView):

    def get(self, request):
        project_id = request.query_params.get("project_id")

        if not project_id:
            return Response(
                {"error": "project_id is required"},
                status=400
            )

        try:
            project = Project.objects.get(
                id=project_id,
                user=request.user
            )
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=404
            )

        if not project.latitude or not project.longitude:
            return Response(
                {"error": "Location not available for this project"},
                status=400
            )

        url = settings.WEATHER_URL

        params = {
            "key": settings.WEATHER_API_KEY,
            "q": f"{project.latitude},{project.longitude}"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            return Response({
                "city": project.city.title if project.city else None,
                "temp_c": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "condition": data["current"]["condition"]["text"],
                "wind_kph": data["current"]["wind_kph"]
            })

        except requests.exceptions.Timeout:
            return Response({"error": "Weather service timeout"}, status=504)

        except requests.exceptions.ConnectionError:
            return Response({"error": "Cannot connect to weather service"}, status=503)

        except requests.exceptions.HTTPError as e:
            return Response({"error": "Weather API error", "detail": str(e)}, status=502)



class ConvertCityToLatlongView(APIView):

    def get(self, request):
        city = request.query_params.get('city')

        if not city:
            return Response(
                {"error": "city query param is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        

        # encode city (for persian names)
        encoded_city = quote(city)

        url = f"{settings.LATLONG_URL}/{encoded_city}?json=1"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()

            lat = data.get('latt')
            lng = data.get('longt')

            if not lat or not lng:
                return Response(
                    {"error": "Location not found for this city"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # update all projects with this city
            Project.objects.filter(city=city).update(
                latitude=lat,
                longitude=lng
            )

            return Response({
                "city": city,
                "latitude": lat,
                "longitude": lng
            })

        except requests.exceptions.Timeout:
            return Response(
                {"error": "LatLong service timeout"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )

        except requests.exceptions.ConnectionError:
            return Response(
                {"error": "Cannot connect to LatLong service"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.HTTPError as e:
            return Response(
                {"error": "LatLong API error", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        except Exception as e:
            return Response(
                {"error": "Unexpected error", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )