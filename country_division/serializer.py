from rest_framework.serializers import ModelSerializer

from country_division.models import Province, City, County, District, Village
from utilities.serializer_helper import CustomSlugRelatedField


class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
        depth = 1


class CitySerializer(ModelSerializer):
    province = CustomSlugRelatedField(slug_field='title', queryset=Province.objects.all(), required=False)

    class Meta:
        model = City
        fields = '__all__'
        depth = 1


class CountySerializer(ModelSerializer):
    city = CustomSlugRelatedField(slug_field='title', queryset=City.objects.all(), required=False)

    class Meta:
        model = County
        fields = '__all__'
        depth = 1


class DistrictSerializer(ModelSerializer):
    county = CustomSlugRelatedField(slug_field='title', queryset=County.objects.all(), required=False)

    class Meta:
        model = District
        fields = '__all__'
        depth = 1


class VillageSerializer(ModelSerializer):
    district = CustomSlugRelatedField(slug_field='title', queryset=District.objects.all(), required=False)

    class Meta:
        model = Village
        fields = '__all__'
        depth = 1
