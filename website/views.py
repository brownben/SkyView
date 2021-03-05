from django.shortcuts import render
from django.http import HttpResponse



# home page
def index(request):
    planets = "<a href='planet/'>planet</a>"
    profile = "<a href='profile/'>profile</a>"
    create_post = "<a href='create_post/'>create_post</a>"
    authenticate = "<a href='authenticate/'>authenticate</a>"
    return HttpResponse("This will be the Homepage " + planets + " " + profile + " " + create_post + " " + authenticate)

# planet page
def planets(request):
    index = "<a href='index/'>Homepage</a>"
    profile = "<a href='profile/'>profile</a>"
    create_post = "<a href='create_post/'>create_post</a>"
    authenticate = "<a href='authenticate/'>authenticate</a>"
    return HttpResponse("This will be a planet page " + index + " " + profile + " " + create_post + " " + authenticate)

# profile page
def profile(request):
    index = "<a href='index/'>Homepage</a>"
    planets = "<a href='planet/'>planet</a>"
    create_post = "<a href='create_post/'>create_post</a>"
    authenticate = "<a href='authenticate/'>authenticate</a>"
    return HttpResponse("This will be the profile page " + index + " " + planets + " " + create_post + " " + authenticate)

# single post page
def post(request):
    
    return HttpResponse("This will be a post page")

# post creation page
def create_post(request):
    index = "<a href='index/'>Homepage</a>"
    planets = "<a href='planet/'>planet</a>"
    profile = "<a href='profile/'>profile</a>"
    authenticate = "<a href='authenticate/'>authenticate</a>"
    return HttpResponse("This will be the page to create posts " + index + " " + planets + " " + profile + " " + authenticate)

# feed page
def feed(request):
    return HttpResponse("This will be the feed page")

# authentication page
def authenticate(request):
    index = "<a href='index/'>Homepage</a>"
    planets = "<a href='planet/'>planet</a>"
    profile = "<a href='profile/'>profile</a>"
    create_post = "<a href='create_post/'>create post</a>"
    return HttpResponse("This will be the page for logging in and signing up " + index + " " + planets + " " + profile + " " + create_post)