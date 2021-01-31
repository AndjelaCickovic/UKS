from django.conf.urls import url
from issues_app import views
from django.urls import path

urlpatterns = [
    url(r'^labels', views.labels, name='view_labels'),
    url(r'^add-label', views.add_label, name='add_label'),
    path('delete-label/<int:label_id>/', views.delete_label, name='delete_label'),
    path('edit-label/<int:label_id>/', views.edit_label, name='edit_label'),
    url(r'^milestones', views.milestones, name='view_milestones'),
    url(r'^add-milestone', views.add_milestone, name='add_milestone'),
    path('delete-milestone/<int:milestone_id>', views.delete_milestone, name='delete_milestone'),
    path('edit-milestone/<int:milestone_id>', views.edit_milestone, name='edit_milestone'),
    path('change-status-milestone/<int:milestone_id>', views.change_status_milestone, name='change_status_milestone'),
    url(r'^$', views.main, name='main')
]