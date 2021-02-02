from django.conf.urls import url
from repositories_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main, name = 'main')
]