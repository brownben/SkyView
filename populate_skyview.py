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
        "data": {
            "averageDistanceFromSun": "57,900,000 km ",
            "diameter": "4,878 km",
            "lengthOfDay": "59 days",
            "lengthOfYear": "88 days",
            "gravitationalFieldStrength": 0.38,
            "averageTemperature": "-183 °C to 427 °C",
            "contentsOfAtmosphere": ["Sodium", "Helium"],
            "numberOfMoons": None,
        },
        "image": "./static/images/mercury.png",
    },
    {
        "name": "Venus",
        "slug": "venus",
        "description": "Another Planet",
        "data": {
            "averageDistanceFromSun": "108,160,000 km",
            "diameter": "12,104 km",
            "lengthOfDay": "243 days",
            "lengthOfYear": "224 days",
            "gravitationalFieldStrength": 0.9,
            "averageTemperature": "480 °C",
            "contentsOfAtmosphere": ["Carbon Dioxide", "Nitrogen"],
            "numberOfMoons": None,
        },
        "image": "./static/images/venus.png",
    },
    {
        "name": "Earth",
        "slug": "earth",
        "description": "The Planet We Live On.",
        "data": {
            "averageDistanceFromSun": "149,600,000 km",
            "diameter": "12,756 km",
            "lengthOfDay": "23 hours, 56 mins",
            "lengthOfYear": "365.25 days",
            "gravitationalFieldStrength": 1,
            "averageTemperature": "14 °C",
            "contentsOfAtmosphere": ["Nitrogen", "Oxygen"],
            "numberOfMoons": 1,
        },
        "image": "./static/images/earth.png",
    },
    {
        "name": "Mars",
        "slug": "mars",
        "description": "The Red Planet.",
        "data": {
            "averageDistanceFromSun": "227,936,640 km",
            "diameter": "6,794 km",
            "lengthOfDay": "24 hours, 37 mins",
            "lengthOfYear": "687 days",
            "gravitationalFieldStrength": 0.38,
            "averageTemperature": "-63 °C",
            "contentsOfAtmosphere": ["Carbon Dioxide", "Argon"],
            "numberOfMoons": 2,
        },
        "image": "./static/images/mars.png",
    },
    {
        "name": "Jupiter",
        "slug": "jupiter",
        "description": "The Biggest Planet.",
        "data": {
            "averageDistanceFromSun": "778,369,000 km",
            "diameter": "142,984 km",
            "lengthOfDay": "9 hours, 55 mins",
            "lengthOfYear": "11.86 years",
            "gravitationalFieldStrength": 2.64,
            "averageTemperature": "-130 °C",
            "contentsOfAtmosphere": ["Hydrogen", "Helium"],
            "numberOfMoons": 79,
        },
        "image": "./static/images/jupiter.png",
    },
    {
        "name": "Saturn",
        "slug": "saturn",
        "description": "The One With Rings.",
        "data": {
            "averageDistanceFromSun": "1,427,034,000 km",
            "diameter": "120,536 km",
            "lengthOfDay": "10 hours, 39 mins",
            "lengthOfYear": "29 years",
            "gravitationalFieldStrength": 1.16,
            "averageTemperature": "-130 °C",
            "contentsOfAtmosphere": ["Hydrogen", "Helium"],
            "numberOfMoons": 82,
        },
        "image": "./static/images/saturn.png",
    },
    {
        "name": "Uranus",
        "slug": "uranus",
        "description": "Cold and Far Away.",
        "data": {
            "averageDistanceFromSun": "2,870,658,186 km",
            "diameter": "51,118 km",
            "lengthOfDay": "17 hours, 14 mins",
            "lengthOfYear": "84 years",
            "gravitationalFieldStrength": 1.11,
            "averageTemperature": "-200 °C",
            "contentsOfAtmosphere": ["Hydrogen", "Helium", "Methane"],
            "numberOfMoons": 27,
        },
        "image": "./static/images/uranus.png",
    },
    {
        "name": "Neptune",
        "slug": "neptune",
        "description": "The Last Planet.",
        "data": {
            "averageDistanceFromSun": "4,496,976,000 km",
            "diameter": "49,532 km",
            "lengthOfDay": "16 hours, 7 mins",
            "lengthOfYear": "164.8 years",
            "gravitationalFieldStrength": 1.21,
            "averageTemperature": "-200 °C",
            "contentsOfAtmosphere": ["Hydrogen", "Helium", "Methane"],
            "numberOfMoons": 14,
        },
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
