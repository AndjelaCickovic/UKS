"""uks_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from users import views as users_views
from myapp import views

urlpatterns = [
    url(r'^users/',include('users.urls')),
    url(r'^myapp/',include('myapp.urls')),
    url(r'^$',users_views.user_login,name='login'),
    url(r'^home',views.index,name='index'),
    url(r'^issues/', include('issues_app.urls')),
    url(r'^wiki/', include('wiki_app.urls')),
    path('admin/', admin.site.urls), 
]
