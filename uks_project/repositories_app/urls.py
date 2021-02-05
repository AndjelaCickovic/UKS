from django.conf.urls import url, include
from repositories_app import views
from django.urls import path

app_name='repositories_app'

urlpatterns = [
    path('repository/<int:repository_id>', views.repository, name= 'view_repository'),
    path('repository/<int:repository_id>/issues/', include('issues_app.urls', namespace='issues_app')),
    path('repository/<int:repository_id>/branches', include('branches_app.urls')),
    path('repository/<int:repository_id>/projects', include('projects_app.urls')),
    path('repository/<int:repository_id>/wiki', include('wiki_app.urls')),
    url(r'^add-repository', views.add_repository, name = 'add_repository'),
    path('edit-repository/<int:repository_id>', views.edit_repository, name = 'edit_repository'),
    path('delete-repository/<int:repository_id>/', views.delete_repository, name='delete_repository'),
    url(r'^$', views.main, name = 'view_repositories'),
]