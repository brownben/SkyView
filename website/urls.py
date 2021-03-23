from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name = 'home'),
    path('Planet/', views.planet, name = 'planet'), # should ideally have name of specific planet
    path('Feed/', views.feed, name = 'feed'),
    path('Feed/NewPost/', views.createPost, name = 'create post'), # this should have the name of the specific planet
    path('Post/<slug:post_name_slug>/', views.post, name = 'view post'),
    path('SignIn/MyProfile', views.profile, name = 'my profile'),
    path('SignUp/', views.signUp, name = 'signUp'),
    path('SignIn/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('Planet/<slug:planet_name_slug>/', \
        views.planet, name='planet'),
]
=======
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("feed/create-post/", views.create_post, name="create_post"),
    path("planets/", views.planets, name="planets"),
    path("planets/<slug:planet_name>/", views.planet, name="planet"),
    path("feed/<slug:post_slug>/", views.post, name="view_post"),
    path("feed/<slug:post_slug>/comment", views.create_comment, name="create_comment"),
    path("feed/<slug:post_slug>/like", views.like_post, name="like_post"),
    path("signUp/", views.sign_up, name="signUp"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("login/my-profile", views.user_profile, name="user_profile"),
]
>>>>>>> 43d545aabdedfc51de9ff79b056e5fd31da2bba4
