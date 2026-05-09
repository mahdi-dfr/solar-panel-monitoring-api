from django.contrib import admin
from .models import Project, Panel, PanelPowerReading

admin.site.register(Project)
admin.site.register(Panel)
admin.site.register(PanelPowerReading)
