import os
import sys

sys.path.append("Skyview/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SkyView.settings")
import django

django.setup()
from django.contrib.auth.models import User

from django.db import models
from django.core.files import File

from website.models import Planet, Post, Comment, Reaction, UserProfile


planets = [
    {
        "name": "Mercury",
        "description": "The Planet Closest to the Sun.",
        "data": {
            "averageDistanceFromSun": "57,900,000 km ",
            "diameter": "4,878 km",
            "lengthOfDay": "59 days",
            "lengthOfYear": "88 days",
            "averageTemperature": "-183 °C to 427 °C",
            "contentsOfAtmosphere": "Sodium, Helium",
            "numberOfMoons": "0",
            "mass": "3.285 x 10^23 kg",
            "volume": "60.8 x 10^9 km^3",
            "water": "in frozen form",
            "gravity": "3.7 m/s^2",
            "specialties": "closest to the sun, smallest planet",
        },
        "image": "./static/images/mercury.png",
    },
    {
        "name": "Venus",
        "description": "Another Planet",
        "data": {
            "averageDistanceFromSun": "108,160,000 km",
            "diameter": "12,104 km",
            "lengthOfDay": "243 days",
            "lengthOfYear": "224 days",
            "averageTemperature": "480 °C",
            "contentsOfAtmosphere": "Carbon Dioxide, Nitrogen",
            "numberOfMoons": "0",
            "mass": "4.867 × 10^24 kg",
            "volume": "9.2843 x 10^11 km^3",
            "water": "no",
            "gravity": "8.87 m/s^2",
            "specialties": "On Venus, a day is longer than a year.",
        },
        "image": "./static/images/venus.png",
    },
    {
        "name": "Earth",
        "description": "The Planet We Live On.",
        "data": {
            "averageDistanceFromSun": "149,600,000 km",
            "diameter": "12,756 km",
            "lengthOfDay": "23 hours, 56 mins",
            "lengthOfYear": "365.25 days",
            "averageTemperature": "14 °C",
            "contentsOfAtmosphere": "Nitrogen, Oxygen",
            "numberOfMoons": "1",
            "mass": "5.972 × 10^24 kg",
            "volume": "1.083 x 10^12 km^3",
            "water": "present in solid, liquid and gaseous form",
            "gravity": "9.81 m/s^2",
            "specialties": "only planet known to contain life",
        },
        "image": "./static/images/earth.png",
    },
    {
        "name": "Mars",
        "description": "The Red Planet.",
        "data": {
            "averageDistanceFromSun": "227,936,640 km",
            "diameter": "6,794 km",
            "lengthOfDay": "24 hours, 37 mins",
            "lengthOfYear": "687 days",
            "averageTemperature": "-63 °C",
            "contentsOfAtmosphere": "Carbon Dioxide, Argon",
            "numberOfMoons": "2",
            "mass": "6.39 × 10^23 kg",
            "volume": "1.631 x 10^11 km^3",
            "water": "in frozen and gaseous form, perhaps in liquid form underneath surface",
            "gravity": "3.711 m/s^2",
            "specialties": "scientists suspect that microorganisms once lived on Mars",
        },
        "image": "./static/images/mars.png",
    },
    {
        "name": "Jupiter",
        "description": "The Biggest Planet.",
        "data": {
            "averageDistanceFromSun": "778,369,000 km",
            "diameter": "142,984 km",
            "lengthOfDay": "9 hours, 55 mins",
            "lengthOfYear": "11.86 years",
            "averageTemperature": "-130 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium",
            "numberOfMoons": "79",
            "mass": "1.898 × 10^27 kg",
            "volume": "1.431 x 10^12 km^3",
            "water": "in gaseous form",
            "gravity": "24.79 m/s^2",
            "specialties": "2.5 times more massive than all other planets in our solar system combined",
        },
        "image": "./static/images/jupiter.png",
    },
    {
        "name": "Saturn",
        "description": "The One With Rings.",
        "data": {
            "averageDistanceFromSun": "1,427,034,000 km",
            "diameter": "120,536 km",
            "lengthOfDay": "10 hours, 39 mins",
            "lengthOfYear": "29 years",
            "averageTemperature": "-130 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium",
            "numberOfMoons": "82",
            "mass": "5.683 × 10^26 kg",
            "volume": "8.271 x 10^11 km^3",
            "water": "scientists suspect small amounts of water beneath surface",
            "gravity": "10.44 m/s^2",
            "specialties": "famous rings are made up of ice, dust and rock",
        },
        "image": "./static/images/saturn.png",
    },
    {
        "name": "Uranus",
        "description": "Cold and Far Away.",
        "data": {
            "averageDistanceFromSun": "2,870,658,186 km",
            "diameter": "51,118 km",
            "lengthOfDay": "17 hours, 14 mins",
            "lengthOfYear": "84 years",
            "averageTemperature": "-200 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium, Methane",
            "numberOfMoons": "27",
            "mass": "8.681 × 10^25 kg",
            "volume": "6.83 x 10^13 km^3",
            "water": "mantle consists of ice",
            "gravity": "8.87 m/s²",
            "specialties": "Uranus was the first planet found using a telescope.",
        },
        "image": "./static/images/uranus.png",
    },
    {
        "name": "Neptune",
        "description": "The Last Planet.",
        "data": {
            "averageDistanceFromSun": "4,496,976,000 km",
            "diameter": "49,532 km",
            "lengthOfDay": "16 hours, 7 mins",
            "lengthOfYear": "164.8 years",
            "averageTemperature": "-200 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium, Methane",
            "numberOfMoons": "14",
            "mass": "1.024 × 10^26 kg",
            "volume": "6.254 x 10^13 km^3",
            "water": "More than 80 percent of the planet's mass is made up of 'icy' materials, including water",
            "gravity": "11.15 m/s²",
            "specialties": "Few people know that Neptune has 5 rings which are made up of dark materials, making them difficult to see.",
        },
        "image": "./static/images/neptune.png",
    },
]

users = [
    {
        "username": "Alice",
        "first_name": "Alice",
        "last_name": "Wilson",
        "email": "alice@gmail.com",
        "password": "HaveFunGoMad",
    },
    {
        "username": "Bob",
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@gmail.com",
        "password": "StapleHorseBattery",
    },
    {
        "username": "c_web",
        "first_name": "Charlotte",
        "last_name": "Webber",
        "email": "c@gmail.com",
        "password": "ThisIsABrilliantPassword",
    },
]

posts = [
    {
        "planet_name": "Earth",
        "heading": "Space Junk? Will We Get Rings Like Saturn?",
        "image": "./static/images/saturn.png",
        "username": "Bob",
        "body": "Lets have a discussion about what we can do to stop the enormous amounts of space junk gathering in Earths Orbit.",
    },
    {
        "planet_name": "Mars",
        "heading": "It Landed!",
        "image": "./static/images/rover.jpg",
        "username": "Bob",
        "body": "The rover managed to land on mars",
    },
    {
        "planet_name": "Jupiter",
        "heading": "This Is My First Post",
        "image": "",
        "username": "c_web",
        "body": "This is my first post on SkyView isn't it really cool",
    },
]

comments = [
    {
        "username": "Alice",
        "post_title": "This Is My First Post",
        "body": "Welcome! Glad You Are Hear!",
    },
    {
        "username": "Alice",
        "post_title": "This Is My First Post",
        "body": "What is your favourite constellation",
    },
    {"username": "c_web", "post_title": "This Is My First Post", "body": "Orion"},
    {
        "username": "Alice",
        "post_title": "It Landed!",
        "body": "Yeah, the landing was gripping. I couldn't focus on any of the other work I had to do",
    },
]

reactions = [
    {"username": "Alice", "post_title": "It Landed!", "reaction_type": "like"},
    {"username": "Bob", "post_title": "It Landed!", "reaction_type": "like"},
    {
        "username": "Alice",
        "post_title": "This Is My First Post",
        "reaction_type": "like",
    },
    {"username": "Bob", "post_title": "This Is My First Post", "reaction_type": "like"},
    {
        "username": "c_web",
        "post_title": "This Is My First Post",
        "reaction_type": "like",
    },
]


def populate():
    for user in users:
        add_user(**user)

    for planet in planets:
        add_planet(**planet)

    for post in posts:
        add_post(**post)

    for comment in comments:
        add_comment(**comment)

    for reaction in reactions:
        add_reaction(**reaction)


def add_user(username, password, first_name, last_name, email):
    new_user = User.objects.get_or_create(username=username)[0]
    new_user.password = password
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.email = email
    new_user.save()

    p = UserProfile.objects.get_or_create(user_id=new_user.id)[0]
    p.save()


def add_planet(name, description, data, image):
    planet = Planet.objects.get_or_create(name=name)[0]
    planet.name = name
    planet.description = description
    planet.data = data

    image_file = File(open(image, "rb"))
    planet.image.save(f"{planet.name}.png", image_file, save=True)

    planet.save()

    print(f"- Added Planet: {planet.name}")
    return planet


def add_post(planet_name, heading, username, image, body):
    planet = Planet.objects.get(name=planet_name)
    creator = User.objects.get(username=username)
    creatorProfile = UserProfile.objects.get(user=creator)

    post = Post.objects.get_or_create(
        heading=heading, planet=planet, creator=creatorProfile
    )[0]
    post.body = body
    post.url_heading = heading.replace(" ", "_")

    if image:
        image_file = File(open(image, "rb"))
        post.image.save(f"{planet.name}.png", image_file, save=True)

    post.save()

    print(f"- Added Post: {heading} by {creator.username} #‎{planet_name}")
    return post


def add_comment(post_title, username, body):
    post = Post.objects.get(heading=post_title)
    creator = User.objects.get(username=username)
    creatorProfile = UserProfile.objects.get(user=creator)

    comment = Comment.objects.get_or_create(post=post, user=creatorProfile, body=body)[
        0
    ]
    comment.save()

    print(f'- Added Comment "{body}" from {username} to the post "{post.heading}"')
    return comment


def add_reaction(post_title, username, reaction_type):
    post = Post.objects.get(heading=post_title)
    creator = User.objects.get(username=username)
    creatorProfile = UserProfile.objects.get(user=creator)

    reaction = Reaction.objects.get_or_create(
        post=post, user=creatorProfile, type=reaction_type
    )[0]
    reaction.save()

    print(
        f'- Added Reaction "{reaction_type}" from {username} to Post "{post.heading}"'
    )
    return reaction


if __name__ == "__main__":
    print("Starting SkyView population script...")
    populate()
