from django.conf.urls import url
from wiki_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main),
    path('page/<int:page_id>/', views.page),
    path('page/edit/<int:page_id>/', views.edit_page),
    path('page/new/', views.new_page),
]