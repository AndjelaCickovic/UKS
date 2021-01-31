from django.contrib import admin
from branches_app.models import Branch, Commit
# Register your models here.

admin.site.register(Branch)
admin.site.register(Commit)