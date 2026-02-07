from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from . serializer import ProjectSerializer, PanelSerializer
from . models import Project, Panel

# Create your views here.

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)    



class PanelViewSet(ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer 

    def perform_create(self, serializer):
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            serializer.save(project=project_id)
        else:
             raise ValidationError(detail={"error": "لطفاً شناسه پروژه (project_id) را از طریق پارامترهای URL ارسال کنید."})



    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            return Panel.objects.filter(project=project_id)    

        else:
            raise ValidationError(detail={"error": "لطفاً شناسه پروژه (project_id) را از طریق پارامترهای URL ارسال کنید."})



# class WeatherView(APIView):
#     def get(self, request, project_id):
        
#         city = Project.objects.get(id=project_id).city
#         print(city)
