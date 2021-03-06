from django.conf.urls import url, include
from repositories_app import views
from django.urls import path

app_name='repositories_app'

urlpatterns = [
    path('search', views.search, name='search_repositories'),
    path('repository/<int:repository_id>', views.repository, name= 'view_repository'),
    path('repository/<int:repository_id>/issues/', include('issues_app.urls', namespace='issues_app')),
    path('repository/<int:repository_id>/branches/', include('branches_app.urls')),
    path('repository/<int:repository_id>/wiki/', include('wiki_app.urls', namespace='wiki_app')),
    path('repository/<int:repository_id>/projects/', include('projects_app.urls', namespace='projects_app')),
    url(r'^add-repository', views.add_repository, name = 'add_repository'),
    path('edit-repository/<int:repository_id>', views.edit_repository, name = 'edit_repository'),
    path('delete-repository/<int:repository_id>/', views.delete_repository, name='delete_repository'),
    path('repository/<int:repository_id>/delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('repository/<int:repository_id>/edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('repository/<int:repository_id>/add-member', views.add_member, name = 'add_member'),
    url(r'^$', views.main, name = 'view_repositories')
]