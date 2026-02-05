from django.db import models


# Create your models here.

class Province(models.Model):
    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان ها'

    title = models.CharField(max_length=50, verbose_name='عنوان')
    code = models.CharField(max_length=10, verbose_name='کد استان', null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title


class City(models.Model):
    class Meta:
        verbose_name = 'شهرستان'
        verbose_name_plural = 'شهرستان ها'

    title = models.CharField(max_length=75, verbose_name='عنوان')
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE, verbose_name='استان')
    code = models.CharField(max_length=20, verbose_name='کد شهر', null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title


class County(models.Model):
    class Meta:
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'

    title = models.CharField(max_length=75, verbose_name='عنوان')
    city = models.ForeignKey(City, related_name='counties', on_delete=models.CASCADE, verbose_name='شهرستان')
    code = models.CharField(max_length=20, verbose_name='کد بخش', null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title


class District(models.Model):
    class Meta:
        verbose_name = 'دهستان'
        verbose_name_plural = 'دهستان ها'

    title = models.CharField(max_length=75, verbose_name='عنوان')
    county = models.ForeignKey(County, related_name='rural_districts', on_delete=models.CASCADE, verbose_name='بخش')
    code = models.CharField(max_length=50, verbose_name='کد دهستان', null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title


class Village(models.Model):
    class Meta:
        verbose_name = 'روستا'
        verbose_name_plural = 'روستا ها'

    title = models.CharField(max_length=75, verbose_name='نام روستا')
    district = models.ForeignKey(District, related_name='villages', on_delete=models.CASCADE,
                                 verbose_name='دهستان')
    code = models.CharField(max_length=50, verbose_name='کد روستا', null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title
