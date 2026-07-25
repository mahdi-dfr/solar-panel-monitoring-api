from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8
    )

    class Meta:

        model = User

        exclude = [
            'groups',
            'user_permissions',
        ]

        extra_kwargs = {

            'username': {
                'required': True,
            },

            'first_name': {
                'required': True,
            },

            'mobile_number': {
                'required': True,
            },
        }

    def create(self, validated_data):

        password = validated_data.pop(
            'password',
            None
        )

        if not password:

            raise serializers.ValidationError({

                'password':
                'Password is required.'
            })

        user = User(
            **validated_data
        )

        user.set_password(
            password
        )

        user.save()

        return user

    def update(
        self,
        instance,
        validated_data
    ):

        password = validated_data.pop(
            'password',
            None
        )

        if password:

            instance.set_password(
                password
            )

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        return instance
    




class SelfUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8
    )

    class Meta:

        model = User

        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'mobile_number',
            'address',
            'email',
            'password',
            'is_staff'
        ]

        read_only_fields = [
            'id',
            'username',
            'mobile_number',
            'is_staff'
        ]

    def update(
        self,
        instance,
        validated_data
    ):

        password = validated_data.pop(
            'password',
            None
        )

        # تغییر پسورد
        if password:

            instance.set_password(
                password
            )

        # تغییر سایر فیلدهای مجاز
        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        return instance