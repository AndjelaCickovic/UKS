from django.contrib import admin
from projects_app.models import Project,Column
# Register your models here.

admin.site.register(Column)
admin.site.register(Project)