from django.contrib import admin
from .models import Project, Board, BoardReading, String, StringReading

admin.site.register(Project)
admin.site.register(Board)
admin.site.register(BoardReading)
admin.site.register(String)
admin.site.register(StringReading)