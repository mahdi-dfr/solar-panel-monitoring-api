from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . serializer import ProjectSerializer, PanelSerializer
from . models import Project, Panel

# Create your views here.



class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer



class PanelViewSet(ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer        