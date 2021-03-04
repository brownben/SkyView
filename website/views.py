from django.shortcuts import render
from django.http import HttpResponse

# home page
def index(request):
    return HttpResponse("This will be the Homepage")

# planet page
def planets(request):
    return HttpResponse("This will be a planet page")

# profile page
def profile(request):
    return HttpResponse("This will be the profile page")

# single post page
def post(request):
    return HttpResponse("This will be a post page")

# post creation page
def create_post(request):
    return HttpResponse("This will be the page to create posts")

# feed page
def feed(request):
    return HttpResponse("This will be the feed page")

# authentication page
def authenticate(request):
    return HttpResponse("This will be the page for logging in and signing up")