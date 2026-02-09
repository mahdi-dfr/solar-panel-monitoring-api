from rest_framework.serializers import ModelSerializer
from .models import Project, Panel
from country_division.serializer import CitySerializer, ProvinceSerializer


class ProjectSerializer(ModelSerializer):
    city = CitySerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    class Meta:
        model= Project
        fields = '__all__'
        read_only_fields = ('user',)

class PanelSerializer(ModelSerializer):
    class Meta:
        model = Panel        
        fields = '__all__'