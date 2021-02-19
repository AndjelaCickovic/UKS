from django.contrib import admin
from issues_app.models import Label, Milestone, Issue

# Register your models here.
admin.site.register(Label)
admin.site.register(Milestone)
admin.site.register(Issue)