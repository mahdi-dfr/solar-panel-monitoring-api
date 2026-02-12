from django.db import models

class Project(models.Model):
    class Meta:
        verbose_name='پروژه'
        verbose_name_plural = 'پروژه ها'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='کاربر', null=False, blank=True, related_name='project_user')
    project_name = models.CharField(max_length=255, verbose_name='نام پروژه', null=False, blank=False)
    project_address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    city = models.ForeignKey('country_division.City', on_delete=models.PROTECT, verbose_name='شهرستان', null=False, blank=False)
    latitude = models.CharField(max_length=255, verbose_name='طول جغرافیایی', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='عرض جغرافیایی', null=True, blank=True)

    province = models.ForeignKey('country_division.Province', on_delete=models.PROTECT, verbose_name='استان', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=False)
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش', blank=False)

    def __str__(self):
        return self.project_name

class Panel(models.Model):
    class Meta:
        verbose_name='پنل'
        verbose_name_plural='پنل ها'

    panel_name =  models.CharField(max_length=255, null=False, blank=False, verbose_name='نام پنل')   
    board_id = models.SmallIntegerField(null=True, blank=False, verbose_name='شناسه ی برد', default=-1, )
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='panel')
    volatge = models.IntegerField(null=True, blank=False, verbose_name='ولتاژ',)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=False)
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش', blank=False)

    def __str__(self):
        return self.panel_name