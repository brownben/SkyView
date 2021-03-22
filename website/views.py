from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from urllib.parse import unquote
from django.urls import reverse

from website.forms import UserForm, UserProfileForm
from website.models import Planet, Post, User, Reaction, Comment, UserProfile

# post creation page
@login_required
def createPost(request):
    return render(request, "SkyView/createPost.html")


# feed page
def feed(request):
    context_dict = {"posts": Post.objects.order_by("time_created")}
    return render(request, "SkyView/feed.html", context=context_dict)


# home page
def home(request):
    contextDict = {
        "recentPosts": Post.objects.order_by("time_created")[:5],
        "isLoggedIn": request.user.is_authenticated,
    }

    return render(request, "SkyView/home.html", context=contextDict)


# planet page
def planet(request, planet_name):
    planetObject = Planet.objects.get(slug=planet_name.lower())
    return render(request, "SkyView/planet.html", context=planetObject.statistics)


# single post page
def post(request, post_name):
    post = Post.objects.get(slug=unquote(post_name))
    likes = Reaction.objects.filter(post=post, type="like")
    comments = Comment.objects.filter(post=post)

    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    user_reaction = Reaction.objects.filter(user=user_profile, post=post).first()

    postDict = {
        "planet": post.planet,
        "heading": post.heading,
        "creator": post.creator,
        "image": post.image,
        "body": post.body,
        "slug": post.slug,
        "timeCreated": post.time_created,
        "numberOfLikes": len(likes),
        "comments": comments,
        "userLikedPost": user_reaction != None,
    }

    return render(request, "SkyView/post.html", context=postDict)


@login_required
def like_post(request, post_name):
    post = Post.objects.get(slug=post_name)

    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    user_reaction = Reaction.objects.filter(user=user_profile, post=post).first()

    if request.method == "POST":
        if user_reaction:
            user_reaction.delete()
            return JsonResponse({"message": "Post Unliked", "buttonText": "Like Post"})
        else:
            Reaction.objects.create(post=post, user=user_profile, type="like")
            return JsonResponse({"message": "Post Liked", "buttonText": "Unlike Post"})
    else:
        return HttpResponse("Invalid Method", 401)


# profile page
@login_required
def profile(request):
    try:
        userPosts = Post.objects.get(creator_id=request.user.id)
    except Post.DoesNotExist:
        userPosts = None
    return render(request, "SkyView/profile.html", userPosts)


# authentication page
def signUp(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # profile picture if available
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "SkyView/signUp.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


def user_login(request):
    if request.method == "POST":
        # Gather the username and password provided by the user
        # check if the combination is valid
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("website:home"))
            else:
                return HttpResponse("Your account is disabled.")

        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        # No context variables to pass to the template system
        return render(request, "SkyView/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("website:home"))
