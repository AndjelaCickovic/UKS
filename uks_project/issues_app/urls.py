from django.conf.urls import url
from issues_app import views

urlpatterns = [
    url(r'^add-label', views.add_label, name='add_label'),
    url(r'^$', views.main, name='main')
]