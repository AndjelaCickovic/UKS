from django.conf.urls import url
from wiki_app import views

urlpatterns = [
    url(r'^$', views.main),
]