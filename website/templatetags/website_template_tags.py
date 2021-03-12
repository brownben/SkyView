from django import template
from website.models import Planet

register = template.Library()


@register.inclusion_tag("SkyView/carousel.html")
def planets_carousel():
    return {"planets": Planet.objects.all()}
