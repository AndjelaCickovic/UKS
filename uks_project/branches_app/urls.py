from django.conf.urls import url
from branches_app import views
from django.urls import path

app_name='branches_app'

urlpatterns = [
    url(r'new',views.new_branch,name='new_branch'),
    url(r'edit/(?P<branch_id>\d+)',views.edit_branch,name='edit_branch'),
    url(r'delete/(?P<branch_id>\d+)',views.delete_branch,name='delete_branch'),
    url(r'add-commit/(?P<branch_id>\d+)',views.new_commit,name='new_commit'),
    url(r'(?P<branch_id>\d+)/commits',views.commits,name='commits'),
    url(r'^$', views.main,name='branches_view')

    # path('new/',views.new_branch),
    # path('edit/<int:branch_id>/',views.edit_branch),
    # path('delete/<int:branch_id>/',views.delete_branch),
    # path('<int:branch_id>/commit/new/',views.new_commit),
    # path('<int:branch_id>/commits',views.commits),
    # path('^$', views.main)
]