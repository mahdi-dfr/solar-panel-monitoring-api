from django.db import models

class Project(models.Model):
    class Meta:
        verbose_name='پروژه'
        verbose_name_plural = 'پروژه ها'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='کاربر', null=False, blank=True, related_name='project_user', default=1)
    project_name = models.CharField(max_length=255, verbose_name='نام پروژه', null=False, blank=False)
    project_address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    city = models.ForeignKey('country_division.City', on_delete=models.PROTECT, verbose_name='شهرستان', null=False, blank=False, default=1)
    latitude = models.CharField(max_length=255, verbose_name='طول جغرافیایی', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='عرض جغرافیایی', null=True, blank=True)
    province = models.ForeignKey('country_division.Province', on_delete=models.PROTECT, verbose_name='استان', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', blank=False)
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش', blank=False)

    def __str__(self):
        return self.project_name



class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boards')
    board_id = models.IntegerField(unique=True)  # همان board_id که از MQTT میاد
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (ID: {self.board_id})"


class String(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='strings')
    string_id = models.IntegerField()  # همان String_id که از MQTT میاد
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('board', 'string_id')

    def __str__(self):
        return f"{self.name} (Board: {self.board.name})"


class BoardReading(models.Model):
    """
    هر بار که پیام MQTT دریافت می‌شه، یک رکورد اینجا ساخته می‌شه.
    دما و رطوبت برد در این جدول ذخیره می‌شن.
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='readings')
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Reading for {self.board.name} at {self.timestamp}"


class StringReading(models.Model):
    """
    مقادیر هر استرینگ مربوط به یک BoardReading.
    توان و انرژی اینجا محاسبه و ذخیره می‌شن.
    """
    board_reading = models.ForeignKey(BoardReading, on_delete=models.CASCADE, related_name='string_readings')
    string = models.ForeignKey(String, on_delete=models.CASCADE, related_name='readings')
    voltage = models.IntegerField()
    current = models.IntegerField()
    power = models.FloatField()   # محاسبه‌شده: voltage * current
    energy = models.FloatField(default=0.0)  # تجمیعی - باید جداگانه مدیریت بشه
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('board_reading', 'string')

    def __str__(self):
        return f"{self.string.name} @ {self.board_reading.timestamp}"