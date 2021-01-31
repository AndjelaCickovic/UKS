from django.conf.urls import url
from projects_app import views

urlpatterns = [
    url(r'^$', views.main, name='main')
]