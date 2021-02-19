from django.conf.urls import url,include
from base_app import views

#TEMPLATE TAGGING
app_name='base_app'

urlpatterns = [
    url(r'^index/$', views.index, name='index')

]

