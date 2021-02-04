from django.conf.urls import url
from wiki_app import views
from django.urls import path

urlpatterns = [
    path('', views.main),
    path('/error', views.error),
    path('/page/<int:page_id>', views.page),
    path('/page/<int:page_id>/edit', views.edit_page),
    path('/page/<int:page_id>/delete', views.delete_page),
    path('/page/new', views.new_page),
]