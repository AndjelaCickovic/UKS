from django.conf.urls import url
from branches_app import views
from django.urls import path

app_name='branches_app'

urlpatterns = [
    url(r'^$', views.main,name='branches_view'),
    url(r'new',views.new_branch,name='branch_view'),
    url(r'(?P<branch_id>\d+)',views.branch)
]