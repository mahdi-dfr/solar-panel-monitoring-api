from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import quote
from django.contrib.auth import get_user_model
from datetime import timedelta

from django.db.models import Avg
from django.db.models.functions import TruncDate
from django.utils import timezone


from rest_framework.views import APIView
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .serializer import (
    ProjectSerializer, LiveBoardSerializer, StringSerializer, BoardSerializer, AdminStatisticsSerializer)

from .models import (
    Project,
    Board,
    String,
    BoardReading,
    StringReading
)
from solar_monitoring_api import settings
import requests

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .models import Project, StringReading

from utilities.utility import get_or_fetch_lat_long
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Prefetch

User = get_user_model()

class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
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


class BoardViewSet(ModelViewSet):

    serializer_class = BoardSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        user = self.request.user

        queryset = Board.objects.select_related(
            'project',
            'project__user'
        ).prefetch_related(
            'strings'
        )

        if user.is_staff:

            return queryset

        return queryset.filter(
            project__user=user
        )

    def perform_create(self, serializer):

        project = serializer.validated_data['project']

        if not self.request.user.is_staff:

            if project.user != self.request.user:

                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    'شما اجازه ساخت برد برای این پروژه را ندارید.'
                )

        serializer.save()


class StringViewSet(ModelViewSet):

    serializer_class = StringSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        user = self.request.user

        queryset = String.objects.select_related(
            'board',
            'board__project',
            'board__project__user'
        )

        if user.is_staff:

            return queryset

        return queryset.filter(
            board__project__user=user
        )

    def perform_create(self, serializer):

        board = serializer.validated_data['board']

        if not self.request.user.is_staff:

            if board.project.user != self.request.user:

                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    'شما اجازه ساخت استرینگ برای این برد را ندارید.'
                )

        serializer.save()


class ProjectLiveDataAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        # گرفتن پروژه
        project = get_object_or_404(
            Project,
            id=project_id
        )

        # چک مالکیت
        if not request.user.is_staff and project.user != request.user:
            return Response(
                {"detail": "شما دسترسی ندارید"},
                status=403
            )

        result = []

        boards = Board.objects.filter(
            project=project
        )

        for board in boards:

            # آخرین reading
            latest_reading = (
                BoardReading.objects
                .filter(board=board)
                .prefetch_related(
                    Prefetch(
                        'string_readings',
                        queryset=StringReading.objects.select_related('string')
                    )
                )
                .order_by('-timestamp')
                .first()
            )

            # اگر هنوز داده‌ای وجود ندارد
            if not latest_reading:
                continue

            result.append({
                "board_id": board.board_id,
                "board_name": board.name,

                "temperature": latest_reading.temperature,
                "humidity": latest_reading.humidity,

                "timestamp": latest_reading.timestamp,

                "strings": latest_reading.string_readings.all()
            })

        serializer = LiveBoardSerializer(result, many=True)

        return Response({
            "project_id": project.id,
            "project_name": project.project_name,
            "boards": serializer.data
        })


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
        

class AdminStatisticsView(APIView):

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        statistics = {

            'total_users': User.objects.count(),

            'total_projects': Project.objects.count(),

            'total_boards': Board.objects.count(),

            'total_strings': String.objects.count(),
        }

        serializer = AdminStatisticsSerializer(
            statistics
        )

        return Response(
            serializer.data
        )


class ProjectDashboardChartView(APIView):

    def get(self, request, project_id):

        period = request.query_params.get(
            'period',
            'week'
        )

        if period not in ['week', 'month']:
            return Response(
                {
                    'detail': 'period must be week or month'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        project = Project.objects.filter(
            id=project_id
        ).first()

        if project is None:
            return Response(
                {
                    'detail': 'پروژه پیدا نشد'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            not request.user.is_staff
            and project.user_id != request.user.id
        ):
            return Response(
                {
                    'detail': 'شما به این پروژه دسترسی ندارید'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        now = timezone.now()

        if period == 'week':
            start_date = now - timedelta(days=7)
        else:
            start_date = now - timedelta(days=30)

        readings = StringReading.objects.filter(
            string__board__project=project,
            board_reading__timestamp__gte=start_date
        )

        chart_data = (
            readings
            .annotate(
                date=TruncDate(
                    'board_reading__timestamp'
                )
            )
            .values('date')
            .annotate(
                average_power=Avg('power'),
                average_energy=Avg('energy'),
                average_voltage=Avg('voltage'),
            )
            .order_by('date')
        )

        data = []

        for item in chart_data:

            data.append(
                {
                    'date': item['date'],
                    'average_power': round(
                        item['average_power'] or 0,
                        2
                    ),
                    'average_energy': round(
                        item['average_energy'] or 0,
                        2
                    ),
                    'average_voltage': round(
                        item['average_voltage'] or 0,
                        2
                    ),
                }
            )

        return Response(
            {
                'period': period,
                'data': data
            },
            status=status.HTTP_200_OK
        )    