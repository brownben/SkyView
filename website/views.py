from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from website.forms import CommentForm, PostForm, UserForm, UserProfileForm
from website.models import Planet, Post, User, Reaction, Comment, UserProfile


def home(request):
    context_dict = {
        "recentPosts": Post.objects.order_by("-time_created")[:5],
        "isLoggedIn": request.user.is_authenticated,
    }

    return render(request, "SkyView/home.html", context=context_dict)


def planets(request):
    context_dict = {"planets": Planet.objects.all()}

    return render(request, "SkyView/planets.html", context=context_dict)


def planet(request, planet_name):
    planet = Planet.objects.get(slug=planet_name)
    posts = Post.objects.filter(planet=planet)

    context_dict = {
        "planet": planet,
        "statistics": planet.statistics,
        "posts": posts,
    }

    return render(request, "SkyView/planet.html", context=context_dict)


def feed(request):
    context_dict = {"posts": Post.objects.order_by("-time_created")}
    return render(request, "SkyView/feed.html", context=context_dict)


def post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    likes = Reaction.objects.filter(post=post, type="like")
    comments = Comment.objects.filter(post=post)

    if request.user.id:
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfile.objects.get(user=user)
        user_reaction = Reaction.objects.filter(user=user_profile, post=post).first()
    else:
        user_reaction = None

    context_dict = {
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

    return render(request, "SkyView/post.html", context=context_dict)


@login_required
def like_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)

    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)
    user_reaction = Reaction.objects.filter(user=user_profile, post=post).first()

    if request.method == "POST":
        if user_reaction:
            user_reaction.delete()
            likes = Reaction.objects.filter(post=post, type="like")
            return JsonResponse(
                {
                    "message": "Post Unliked",
                    "buttonText": "Like this Post",
                    "liked": False,
                    "numberOfLikes": len(likes),
                }
            )
        else:
            Reaction.objects.create(post=post, user=user_profile, type="like")
            likes = Reaction.objects.filter(post=post, type="like")
            return JsonResponse(
                {
                    "message": "Post Liked",
                    "buttonText": "You Like this Post",
                    "liked": True,
                    "numberOfLikes": len(likes),
                }
            )
    else:
        return HttpResponse("Invalid Method", 401)


@login_required
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            user = User.objects.get(id=request.user.id)
            user_profile = UserProfile.objects.get(user=user)
            post.creator = user_profile

            post.save()
            return redirect("/feed")
    else:
        return render(request, "SkyView/createPost.html", {"form": form})


@login_required
def create_comment(request, post_slug):
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        post = None

    if post is None:
        return redirect("/")

    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            if post:
                comment = form.save(commit=False)

                comment.post = post
                comment.user = user_profile

                comment.save()

                return redirect(
                    reverse(
                        "website:view_post",
                        kwargs={"post_slug": post_slug},
                    )
                )

    form = CommentForm()
    context_dict = {"form": form, "post": post}

    return render(request, "SkyView/createComment.html", context=context_dict)


@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=user)

    try:
        userPosts = Post.objects.filter(creator_id=request.user.id)
    except Post.DoesNotExist:
        userPosts = None

    context_dict = {"userPosts": userPosts, "userProfile": user_profile}
    return render(request, "SkyView/profile.html", context=context_dict)


def sign_up(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES)

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
