from django.conf.urls import url
from projects_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main, name='main'),
    path('new/', views.new_project),
    path('close/<int:project_id>/',views.close_project),
    path('reopen/<int:project_id>/',views.reopen_project),
]