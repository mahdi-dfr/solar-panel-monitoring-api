from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from country_division.models import County, City, District, Village, Province
from country_division.serializer import CitySerializer, CountySerializer, DistrictSerializer, VillageSerializer, \
    ProvinceSerializer
from utilities.utility import SelectMixIn
from utilities.views_helper import DestroyProtectedMixin


# Create your views here.

class ProvinceViewSet(DestroyProtectedMixin, ModelViewSet, SelectMixIn):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all().order_by('title')
    filterset_fields = ['title']
    select_text_field = 'title'
    ordering_fields = "__all__"


class CityViewSet(DestroyProtectedMixin, ModelViewSet, SelectMixIn):
    serializer_class = CitySerializer
    queryset = City.objects.all().order_by('title')
    select_text_field = 'title'
    filterset_fields = ['title', 'province']
    ordering_fields = "__all__"


class CountyViewSet(DestroyProtectedMixin, ModelViewSet, SelectMixIn):
    serializer_class = CountySerializer
    queryset = County.objects.all().order_by('title')
    select_text_field = 'title'
    filterset_fields = ['city']
    ordering_fields = "__all__"


class DistrictViewSet(DestroyProtectedMixin, ModelViewSet, SelectMixIn):
    serializer_class = DistrictSerializer
    queryset = District.objects.all().order_by('title')
    select_text_field = 'title'
    filterset_fields = ['title', 'county']
    ordering_fields = "__all__"


class VillageViewSet(DestroyProtectedMixin, ModelViewSet, SelectMixIn):
    serializer_class = VillageSerializer
    queryset = Village.objects.all().order_by('title')
    select_text_field = 'title'
    filterset_fields = ['title', 'district']
    ordering_fields = "__all__"
