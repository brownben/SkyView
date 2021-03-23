from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("feed/create-post/", views.createPost, name="create-post"),
    path("planets/", views.planets, name="planets"),
    path("planets/<slug:planet_name>/", views.planet, name="planet"),
    path("feed/<slug:post_slug>/", views.post, name="view-post"),
    path("feed/<slug:post_slug>/comment", views.create_comment, name="create_comment"),
    path("feed/<slug:post_slug>/like", views.like_post, name="like_post"),
    path("sign-in/", views.user_login, name="login"),
    path("sign-in/my-profile", views.profile, name="my profile"),
    path("sign-up/", views.signUp, name="signUp"),
    path("logout/", views.user_logout, name="logout"),
]
