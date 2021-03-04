"""SkyView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include
from website import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create_post/', views.create_post, name = 'create_post'),
    path('feed/', views.feed, name = 'feed'),
    path('planet/', views.planets, name = 'planet'), # this should have the name of the specific planet
    path('view_post/', views.post, name = 'view_post'),
    path('profile/', views.profile, name = 'profile'),
    path('authenticate/', views.authenticate, name = 'authenticate'),
    path('admin/', admin.site.urls),
    path('website/', include('website.urls')),
]
