from rest_framework import serializers
from . models import User
from utilities.serializer_helper import DisplayTextChoicesField
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['password', 'groups', 'user_permissions']
        model = User

    
    def validate_password(self, value):
        return make_password(value)    