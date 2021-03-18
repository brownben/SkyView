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
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "Planet/", views.planet, name="planet"
    ),  # should ideally have name of specific planet
    path("Feed/", views.feed, name="feed"),
    path(
        "Feed/NewPost/", views.createPost, name="create post"
    ),  # this should have the name of the specific planet
    path('Post/<str:post_name>/', views.post, name = 'view post'),
    path('SignIn/', views.user_login, name='login'),
    path("SignIn/MyProfile", views.profile, name="my profile"),
    path("SignUp/", views.signUp, name="sign up"),
    path("admin/", admin.site.urls),
    path("website/", include("website.urls")),
    path('Planet/<slug:planet_name_slug>/', \
        views.planet, name='planet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
