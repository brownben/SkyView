from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# post creation page
@login_required
def createPost(request):
    return render(request, 'SkyView/createPost.html')

# feed page
def feed(request):
    return render(request, 'SkyView/feed.html')

# home page
def home(request):
    return render(request, 'SkyView/home.html')

# planet page
def planet(request):    
    return render(request, 'SkyView/planet.html')

# single post page
def post(request):
    return render(request, 'SkyView/post.html')

# profile page
@login_required
def profile(request):
    return render(request, 'SkyView/profile.html')

# authentication page
def signUp(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # profile picture if available
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

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

    return render(request, 'SkyView/signUp.html',
                context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user
        # check if the combination is valid
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('website:home'))
            else:
                return HttpResponse("Your account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        
    else:
        # No context variables to pass to the template system
        return render(request, 'SkyView/login.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('website:home'))