import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SkyView.settings")
import django

django.setup()
from website.models import Planet, Post, Comment, Reaction

planets = [
    {
        "name": "Mercury",
        "slug": "mercury",
        "description": "The Planet Closest to the Sun.",
        "data": "",
    },
    {
        "name": "Venus",
        "slug": "venus",
        "description": "Another Planet",
        "data": "",
    },
    {
        "name": "Earth",
        "slug": "earth",
        "description": "The Planet We Live On.",
        "data": "",
    },
    {
        "name": "Mars",
        "slug": "mars",
        "description": "The Red Planet.",
        "data": "",
    },
    {
        "name": "Jupiter",
        "slug": "jupiter",
        "description": "The Biggest Planet.",
        "data": "",
    },
    {
        "name": "Saturn",
        "slug": "saturn",
        "description": "The One With Rings.",
        "data": "",
    },
    {
        "name": "Uranus",
        "slug": "uranus",
        "description": "Cold and Far Away.",
        "data": "",
    },
]


def populate():
    for planet in planets:
        add_planet(**planet)


def add_planet(name, slug, description, data):
    planet = Planet.objects.get_or_create(
        name=name, slug=slug, description=description, data=data
    )[0]
    planet.save()
    return planet


if __name__ == "__main__":
    print("Starting SkyView population script...")
    populate()
