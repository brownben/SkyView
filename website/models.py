from django.db import models
from django.contrib.auth.models import User
import json

slug = models.SlugField(unique=True)

class Planet(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    description = models.TextField()
    data = models.TextField()
    image = models.ImageField(upload_to="planets", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if type(self.data) != type(""):
            self.data = json.dumps(self.data)

        super().save(*args, **kwargs)

    @property
    def statistics(self):
        if type(self.data) == type(""):
            return json.loads(self.data)
        else:
            return self.data


class Post(models.Model):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    heading = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts", blank=True)
    body = models.TextField()
    slug = models.SlugField()
    time_created = models.DateTimeField()

    def __str__(self):
        return self.heading


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    time_created = models.DateTimeField()

    def __str__(self):
        return self.id


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    body = models.TextField()

    def __str__(self):
        return self.id


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return self.user.username