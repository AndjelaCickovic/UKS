from django.contrib import admin
from repositories_app.models import Repository, RepositoryUser

# Register your models here.
admin.site.register(Repository)
admin.site.register(RepositoryUser)