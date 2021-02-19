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
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
from base_app import views



urlpatterns = [
    url(r'^users/',include('users.urls')),
    url(r'^base_app/',include('base_app.urls')),
    url(r'^$',views.index,name='index'),
    url(r'^home',views.index,name='index'),
    url(r'^issues/', include('issues_app.urls')),
    url(r'^wiki/', include('wiki_app.urls')),
    url(r'^projects/',include('projects_app.urls')),
    url(r'^branches/', include('branches_app.urls')),
    url(r'^repositories/', include('repositories_app.urls')),
    path('admin/', admin.site.urls), 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)