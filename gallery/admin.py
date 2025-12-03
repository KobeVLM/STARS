from django.contrib import admin
from .models import Artwork, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'artist__username')
    filter_horizontal = ('tags',)
