from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.validators import *

# Create your models here.

class User(AbstractUser):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    address = models.CharField(max_length=255, null=True, blank=True)

    mobile_number = models.CharField(
        max_length=11,
        validators=[mobile_validator],
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username