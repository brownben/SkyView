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
            "averageTemperature": "-183 °C to 427 °C",
            "contentsOfAtmosphere": "Sodium, Helium",
            "numberOfMoons": "0",
            "mass" : "3.285 x 10^23 kg",
            "volume" : "60.8 x 10^9 km^3",
            "water" : "in frozen form",
            "gravity" : "3.7 m/s^2",
            "specialties" : "closest to the sun, smallest planet"
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
            "averageTemperature": "480 °C",
            "contentsOfAtmosphere": "Carbon Dioxide, Nitrogen",
            "numberOfMoons": "0",
            "mass" : "4.867 × 10^24 kg",
            "volume" : "9.2843 x 10^11 km^3",
            "water" : "no",
            "gravity" : "8.87 m/s^2",
            "specialties" : "On Venus, a day is longer than a year."

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
            "averageTemperature": "14 °C",
            "contentsOfAtmosphere": "Nitrogen, Oxygen",
            "numberOfMoons": "1",
            "mass" : "5.972 × 10^24 kg",
            "volume" : "1.083 x 10^12 km^3",
            "water" : "present in solid, liquid and gaseous form",
            "gravity" : "9.81 m/s^2",
            "specialties" : "only planet known to contain life"
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
            "averageTemperature": "-63 °C",
            "contentsOfAtmosphere": "Carbon Dioxide, Argon",
            "numberOfMoons": "2",
            "mass" : "6.39 × 10^23 kg",
            "volume" : "1.631 x 10^11 km^3",
            "water" : "in frozen and gaseous form, perhaps in liquid form underneath surface",
            "gravity" : "3.711 m/s^2",
            "specialties" : "scientists suspect that microorganisms once lived on Mars"
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
            "averageTemperature": "-130 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium",
            "numberOfMoons": "79",
            "mass" : "1.898 × 10^27 kg",
            "volume" : "1.431 x 10^12 km^3",
            "water" : "in gaseous form",
            "gravity" : "24.79 m/s^2",
            "specialties" : "2.5 times more massive than all other planets in our solar system combined"
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
            "averageTemperature": "-130 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium",
            "numberOfMoons": "82",
            "mass" : "5.683 × 10^26 kg",
            "volume" : "8.271 x 10^11 km^3",
            "water" : "scientists suspect small amounts of water beneath surface",
            "gravity" : "10.44 m/s^2",
            "specialties" : "famous rings are made up of ice, dust and rock"
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
            "averageTemperature": "-200 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium, Methane",
            "numberOfMoons": "27",
            "mass" : "8.681 × 10^25 kg",
            "volume" : "6.83 x 10^13 km^3",
            "water" : "mantle consists of ice",
            "gravity" : "8.87 m/s²",
            "specialties" : "Uranus was the first planet found using a telescope."
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
            "averageTemperature": "-200 °C",
            "contentsOfAtmosphere": "Hydrogen, Helium, Methane",
            "numberOfMoons": "14",
            "mass" : "1.024 × 10^26 kg",
            "volume" : "6.254 x 10^13 km^3",
            "water" : "More than 80 percent of the planet's mass is made up of 'icy' materials, including water",
            "gravity" : "11.15 m/s²",
            "specialties" : "Few people know that Neptune has 5 rings which are made up of dark materials, making them difficult to see."
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