from django.contrib import admin
from .models import Like, Comment, Report, CommentFlag


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


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'reporter', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('reporter__username', 'artwork__title', 'description')


@admin.register(CommentFlag)
class CommentFlagAdmin(admin.ModelAdmin):
    list_display = ('comment', 'flagged_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('flagged_by__username', 'comment__content')
