"""Coding_Machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Engine.view_dir import views, views_user
from Engine.view_dir import views_folder

urlpatterns = [
    # url(r'^main/', views.main, name="main"),

    # views for user
    url(r'^$', views_user.login_view, name="login"),
    url(r'^logout/', views_user.logout_view, name="logout"),
    # views for coding
    url(r'^coding/', views.coding, name="coding"),
    url(r'^save/', views.save, name="save"),
    url(r'^run/', views.result, name="run"),
    # views for folder control
    url(r'^folder/$', views_folder.find_folder, name="folder"),
    url(r'^folder/make/', views_folder.make_folder, name="make_folder"),
    url(r'^folder/delete/', views_folder.delete_folder, name="delete_folder"),
    url(r'^admin/', admin.site.urls),

]
urlpatterns += staticfiles_urlpatterns()
