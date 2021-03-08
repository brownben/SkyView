from django.contrib import admin
from .models import Planet, Post, Reaction, Comment, UserProfile


admin.site.register(Planet)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Comment)
