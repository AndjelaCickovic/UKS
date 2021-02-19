from django.conf.urls import url,include
from users import views

#TEMPLATE TAGGING
app_name='users'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',views.user_login,name='user_login'),
    url(r'^logout/$',views.user_logut,name='user_logout'),
    url(r'^edit/profile$',views.edit_profile,name='edit_profile'),

]