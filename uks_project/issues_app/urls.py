from django.conf.urls import url
from issues_app import views
from django.urls import path

urlpatterns = [
    url(r'^labels', views.labels, name='view_labels'),
    url(r'^add-label', views.add_label, name='add_label'),
    path('delete-label/<int:label_id>/', views.delete_label, name='delete_label'),
    path('edit-label/<int:label_id>/', views.edit_label, name='edit_label'),
    url(r'^$', views.main, name='main')
]