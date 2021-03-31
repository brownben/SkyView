from django.contrib import admin
from .models import Planet, Post, Reaction, Comment, UserProfile


class PlanetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("heading",)}


class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("user",)}


admin.site.register(Planet, PlanetAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reaction)
admin.site.register(Comment)
