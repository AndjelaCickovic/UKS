from django.conf.urls import url
from projects_app import views
from django.urls import path

app_name='projects_app'


urlpatterns = [
    url(r'^$', views.main, name='main'),
    path('<int:project_id>/',views.project, name='project'),
    path('<int:project_id>/delete_column/<int:column_id>',views.delete_column),
    path('<int:project_id>/edit_column/<int:column_id>',views.edit_column),
    path('<int:project_id>/new_column/',views.new_column),
    path('<int:project_id>/<int:column_id>/new_issue',views.new_issue),
    path('<int:project_id>/edit_issue/<int:issue_id>',views.edit_issue),
    path('<int:project_id>/change_column_issue/<int:issue_id>',views.change_column_issue),
    path('<int:project_id>/delete_issue/<int:issue_id>',views.delete_issue),
    path('<int:project_id>/remove_issue/<int:issue_id>',views.remove_issue),
    path('new/', views.new_project,name="new_project"),
    path('close/<int:project_id>/',views.close_project,name='close_project'),
    path('reopen/<int:project_id>/',views.reopen_project, name='reopen_project'),
    path('edit/<int:project_id>/',views.edit_project),
    path('delete/<int:project_id>/',views.delete_project,name="delete_project"),
]