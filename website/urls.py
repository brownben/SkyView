from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "planet/", views.planet, name="planet"
    ),  # should ideally have name of specific planet
    path("feed/", views.feed, name="feed"),
    path(
        "feed/new-post/", views.createPost, name="create-post"
    ),  # this should have the name of the specific planet
    path("feed/<slug:post_name_slug>/", views.post, name="view-post"),
    path("sign-in/my-profile", views.profile, name="my profile"),
    path("sign-up/", views.signUp, name="signUp"),
    path("sign-in/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("planet/<slug:planet_name_slug>/", views.planet, name="planet"),
]
