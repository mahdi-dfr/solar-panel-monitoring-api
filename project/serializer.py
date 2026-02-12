from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Project, Panel
from country_division.models import City
from country_division.serializer import CitySerializer


class ProjectSerializer(ModelSerializer):
    
    # برای دریافت city هنگام create
    city = PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=True,
        allow_null=False,
    )

    # برای نمایش اطلاعات شهر هنگام GET
    # city_detail = CitySerializer(source='city', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('user',)
        


class PanelSerializer(ModelSerializer):
    class Meta:
        model = Panel        
        fields = '__all__'