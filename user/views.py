from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . models import User
from . serializer import UserSerializer
from rest_framework.permissions import IsAdminUser
from ACU.custom_permissions import IsOwner


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):

        if self.request.user.is_staff:
            return User.objects.all()

        return User.objects.filter(
            id=self.request.user.id
        )
    
