from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.validators import *

# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    first_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام', )    
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی', null=False, blank=False)
    address = models.CharField(max_length=255, verbose_name='آدرس', null=True, blank=True)
    mobile_number = models.CharField(max_length=11, verbose_name='شماره موبایل', null=False, blank=False,
                                     validators=[mobile_validator], )
    ROLE_LIST = [(1, 'ادمین') , (2 , 'کاربرعادی'), ]
    role = models.CharField(max_length=1, default='0', choices=ROLE_LIST, verbose_name='نقش کاربر', )
    
    last_login = models.DateTimeField(auto_now=True, blank=True, verbose_name='آخرین ورود')
    create_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ تغییر')

    def __str__(self):
        return self.username