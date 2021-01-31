from django.conf.urls import url
from projects_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main, name='main'),
    path('new/', views.new_project),
]