from django.urls import path
from website import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('Planet/', views.planet, name = 'planet'), # should ideally have name of specific planet
    path('Feed/', views.feed, name = 'feed'),
    path('Feed/NewPost/', views.createPost, name = 'create post'), # this should have the name of the specific planet
    path('Post/', views.post, name = 'view post'),
    path('SignIn/MyProfile', views.profile, name = 'my profile'),
    path('SignUp/', views.signUp, name = 'signUp'),
    path('SignIn/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('Planet/<slug:planet_name_slug>/', \
        views.planet, name='planet'),
]