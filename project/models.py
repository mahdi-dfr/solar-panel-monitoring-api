from django.db import models

class Project(models.Model):
    class Meta:
        verbose_name='پروژه'
        verbose_name_plural = 'پروژه ها'

    project_name = models.CharField(max_length=255, verbose_name='نام پروژه', null=False, blank=False)
    project_address = models.TextField(null=False, blank=False, verbose_name='آدرس')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=False)
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش', blank=False)


class Panel(models.Model):
    class Meta:
        verbose_name='پنل'
        verbose_name_plural='پنل ها'

    panel_name =  models.CharField(max_length=255, null=False, blank=False, verbose_name='نام پنل')   
    board_id = models.SmallIntegerField(verbose_name='شناسه ی برد', blank=True, default=1)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='panel')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=False)
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش', blank=False)
