from django import template
from website.models import Planet, Post, Comment

register = template.Library()


@register.inclusion_tag("SkyView/partials/carousel.html")
def planets_carousel():
    return {"planets": Planet.objects.all()}


@register.inclusion_tag("SkyView/partials/comment.html")
def comment(comment):
    return {"comment": Comment.objects.get(id=comment)}


@register.inclusion_tag("SkyView/partials/feedItem.html")
def feedItem(post):
    return {"post": Post.objects.get(slug=post)}
