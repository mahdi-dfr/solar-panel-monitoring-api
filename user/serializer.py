from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

        extra_kwargs = {
            'first_name': {'required': True},
            'mobile_number': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user