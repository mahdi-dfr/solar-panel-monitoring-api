from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

from .serializer import (
    AdminUserSerializer,
    SelfUserSerializer,
)

from .permissions import UserPermission


User = get_user_model()


class UserViewSet(ModelViewSet):

    permission_classes = [
        UserPermission
    ]

    def get_queryset(self):

        user = self.request.user

        # ادمین
        if user.is_staff:

            return User.objects.all()

        # کاربر عادی فقط خودش
        return User.objects.filter(
            id=user.id
        )

    def get_serializer_class(self):

        # ادمین
        if self.request.user.is_staff:

            return AdminUserSerializer

        # کاربر عادی
        return SelfUserSerializer