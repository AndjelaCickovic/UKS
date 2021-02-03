from django.conf.urls import url, include
from repositories_app import views
from django.urls import path

app_name='repositories_app'

urlpatterns = [
    path('repository/<int:repository_id>', views.repository, name= 'view_repository'),
    path('repository/<int:repository_id>/issues', include('issues_app.urls')),
    path('repository/<int:repository_id>/branches', include('branches_app.urls')),
    path('repository/<int:repository_id>/projects', include('projects_app.urls')),
    path('repository/<int:repository_id>/wiki', include('wiki_app.urls')),
    url(r'^$', views.main, name = 'main'),
]