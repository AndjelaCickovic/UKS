from django.conf.urls import url
from wiki_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main),
    path('page/<int:page_id>/', views.page),
]