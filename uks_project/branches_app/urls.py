from django.conf.urls import url
from branches_app import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.main),
    path('branch/<int:branch_id>/', views.branch),
]