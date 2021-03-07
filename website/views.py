from django.shortcuts import render
from django.http import HttpResponse


# post creation page
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
def profile(request):
    return render(request, 'SkyView/profile.html')

# authentication page
def signUp(request):
    return render(request, 'SkyView/signUp.html')