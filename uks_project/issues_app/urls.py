from django.conf.urls import url
from issues_app import views
from django.urls import path

app_name='issues_app'

urlpatterns = [
    url('labels', views.labels, name='view_labels'),
    url('add-label', views.add_label, name='add_label'),
    url(r'delete-label/(?P<label_id>\d+)', views.delete_label, name='delete_label'),
    url(r'edit-label/(?P<label_id>\d+)', views.edit_label, name='edit_label'),
    url('milestones', views.milestones, name='view_milestones'),
    url('add-milestone', views.add_milestone, name='add_milestone'),
    url(r'delete-milestone/(?P<milestone_id>\d+)', views.delete_milestone, name='delete_milestone'),
    url(r'edit-milestone/(?P<milestone_id>\d+)', views.edit_milestone, name='edit_milestone'),
    url(r'change-status-milestone/(?P<milestone_id>\d+)', views.change_status_milestone, name='change_status_milestone'),
    url(r'issue/(?P<issue_id>\d+)', views.issue, name='view_issue'),
    url('add-issue', views.add_issue, name='add_issue'),
    url(r'edit-issue/(?P<issue_id>\d+)', views.edit_issue, name='edit_issue'),
    url(r'delete-issue/(?P<issue_id>\d+)', views.delete_issue, name='delete_issue'),
    url(r'change-status-issue/(?P<issue_id>\d+)', views.change_status_issue, name='change_status_issue'),
    url(r'^$', views.main, name='view_issues')
]