import datetime
import os

from django.db.models import ProtectedError, Sum
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Sum, Value, FloatField
from django.db.models.functions import Coalesce

from user.models import User
from .utility import get_file_content_type


class SavingByRoleMixin:
    """
    This mixin class used in ViewSets,
    we override perform_create() and perform_update().
    this class prevent from duplicate role check in saving objects.
    """

    def _perform_by_role(self, serializer):
        _user = self.request.user

        # if province_office try to save an object. that object must be in same province automatically.
        if _user.role == '2':
            # the province_office must have province
            if _user.province:
                return serializer.save(province=_user.province)
            else:
                raise ValidationError('استانی برای شما تعریف نشده است!')

        return serializer.save()

    def perform_create(self, serializer):
        return self._perform_by_role(serializer)

    def perform_update(self, serializer):
        return self._perform_by_role(serializer)


class DestroyProtectedMixin(DestroyModelMixin):
    """
    When we want to delete a protected object. it has potential to raise ProtectedError exception.
    This class should only be used together with the DestroyMixin class.
    """

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            raise ValidationError('این مورد به دلیل استفاده شدن توسط دیگر اشیا قابل حذف نیست!')


