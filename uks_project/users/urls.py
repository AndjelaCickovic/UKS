from django.conf.urls import url,include
from users import views

#TEMPLATE TAGGING
app_name='users'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',views.login,name='login')
]