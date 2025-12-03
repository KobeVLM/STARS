from django.contrib import admin
from .models import Like, Comment


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'artwork__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'artwork__title', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
