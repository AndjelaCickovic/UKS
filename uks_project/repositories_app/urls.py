from django.conf.urls import url
from repositories_app import views
from django.urls import path

urlpatterns = [
    path('repository/<int:repository_id>', views.repository, name= 'view_repository'),
    url(r'^$', views.main, name = 'main'),
]