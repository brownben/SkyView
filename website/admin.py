from django.contrib import admin
from .models import Planet, Post, Reaction, Comment, UserProfile

class PlanetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name", )}

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("heading", )}

admin.site.register(Planet, PlanetAdmin)
admin.site.register(UserProfile)
admin.site.register(Post, PostAdmin)
admin.site.register(Reaction)
admin.site.register(Comment)