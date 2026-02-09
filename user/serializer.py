from rest_framework import serializers
from . models import User
from utilities.serializer_helper import DisplayTextChoicesField

class UserSerializer(serializers.ModelSerializer):
    role = DisplayTextChoicesField(choices=User.ROLE_LIST , required=True)

    class Meta:
        exclude = ['password', 'groups', 'user_permissions']
        model = User