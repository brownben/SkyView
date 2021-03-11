import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SkyView.settings")
import django
from django.db import models
from django.core.files import File

django.setup()
from website.models import Planet, Post, Comment, Reaction


planets = [
    {
        "name": "Mercury",
        "slug": "mercury",
        "description": "The Planet Closest to the Sun.",
        "data": "",
        "image": "./static/images/mercury.png",
    },
    {
        "name": "Venus",
        "slug": "venus",
        "description": "Another Planet",
        "data": "",
        "image": "./static/images/venus.png",
    },
    {
        "name": "Earth",
        "slug": "earth",
        "description": "The Planet We Live On.",
        "data": "",
        "image": "./static/images/earth.png",
    },
    {
        "name": "Mars",
        "slug": "mars",
        "description": "The Red Planet.",
        "data": "",
        "image": "./static/images/mars.png",
    },
    {
        "name": "Jupiter",
        "slug": "jupiter",
        "description": "The Biggest Planet.",
        "data": "",
        "image": "./static/images/jupiter.png",
    },
    {
        "name": "Saturn",
        "slug": "saturn",
        "description": "The One With Rings.",
        "data": "",
        "image": "./static/images/saturn.png",
    },
    {
        "name": "Uranus",
        "slug": "uranus",
        "description": "Cold and Far Away.",
        "data": "",
        "image": "./static/images/uranus.png",
    },
    {
        "name": "Neptune",
        "slug": "neptune",
        "description": "The Last Planet.",
        "data": "",
        "image": "./static/images/neptune.png",
    },
]


def populate():
    for planet in planets:
        add_planet(**planet)


def add_planet(name, slug, description, data, image):
    planet = Planet.objects.get_or_create(
        name=name, slug=slug, description=description, data=data
    )[0]
    planet.name = name
    planet.description = description
    planet.data = data

    image_file = File(open(image, "rb"))
    planet.image.save(f"{planet.name}.png", image_file, save=True)

    planet.save()

    print(f"- Added Planet: {planet.name}")
    return planet


if __name__ == "__main__":
    print("Starting SkyView population script...")
    populate()
