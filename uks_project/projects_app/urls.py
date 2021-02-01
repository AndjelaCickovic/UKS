from django.conf.urls import url
from projects_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main, name='main'),
    path('<int:project_id>/',views.project),
    path('<int:project_id>/delete_column/<int:column_id>',views.delete_column),
    path('<int:project_id>/edit_column/<int:column_id>',views.edit_column),
    path('<int:project_id>/new_column/',views.new_column),
    path('new/', views.new_project),
    path('close/<int:project_id>/',views.close_project),
    path('reopen/<int:project_id>/',views.reopen_project),
    path('edit/<int:project_id>/',views.edit_project),
    path('delete/<int:project_id>/',views.delete_project),
]