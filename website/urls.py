from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
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