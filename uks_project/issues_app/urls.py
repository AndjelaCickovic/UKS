from django.conf.urls import url
from issues_app import views

urlpatterns = [
    url(r'^$', views.main, name='main')
]