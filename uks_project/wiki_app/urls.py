from django.conf.urls import url
from wiki_app import views
from django.urls import path

app_name='wiki_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('error', views.error, name='error'),
    path('page/<int:page_id>', views.page, name='page'),
    path('page/<int:page_id>/edit', views.edit_page, name='edit'),
    path('page/<int:page_id>/delete', views.delete_page, name='delete'),
    path('page/new', views.new_page, name='new'),
]