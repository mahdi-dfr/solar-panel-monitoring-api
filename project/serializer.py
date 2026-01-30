from rest_framework.serializers import ModelSerializer
from .models import Project, Panel


class ProjectSerializer(ModelSerializer):
    class Meta:
        model= Project
        fields = '__all__'

class PanelSerializer(ModelSerializer):
    class Meta:
        model = Panel        
        fields = '__all__'