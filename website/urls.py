from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path(
        "feed/new-post/", views.createPost, name="create-post"
    ),  # this should have the name of the specific planet
    path(
        "planet/", views.planet, name="planet"
    ),  # should ideally have name of specific planet
    path("planet/<slug:planet_name>/", views.planet, name="planet"),
    path("feed/<slug:post_name>/", views.post, name="view-post"),
    path("feed/<slug:post_name>/like", views.like_post, name="like_post"),
    path("sign-in/", views.user_login, name="login"),
    path("sign-in/my-profile", views.profile, name="my profile"),
    path("sign-up/", views.signUp, name="signUp"),
    path("logout/", views.user_logout, name="logout"),
]
