from django.conf.urls import url
from branches_app import views
from django.urls import path

app_name='branches_app'

urlpatterns = [
    url(r'^$', views.main,name='branches_view'),
    url(r'new',views.new_branch,name='new_branch'),
    url(r'edit/(?P<branch_id>\d+)',views.edit_branch,name='edit_branch'),
    url(r'delete/(?P<branch_id>\d+)',views.delete_branch,name='delete_branch'),
    url(r'(?P<branch_id>\d+)',views.commits,name='commits')
]