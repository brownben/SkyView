from django.contrib import admin
from .models import Planet, Post, Reaction, Comment, UserProfile

class PlanetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name", )}

admin.site.register(Planet, PlanetAdmin)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Comment)
