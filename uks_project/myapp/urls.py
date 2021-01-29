from django.conf.urls import url,include
from myapp import views

#TEMPLATE TAGGING
app_name='myapp'

urlpatterns = [
    url(r'^index/$', views.index, name='index')

]

