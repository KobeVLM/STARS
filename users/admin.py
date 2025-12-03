from django.contrib import admin
from .models import CustomUser, Badge, UserBadge


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'level', 'xp', 'date_joined')
    list_filter = ('level', 'date_joined')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'criteria_type', 'criteria_value', 'created_at')
    list_filter = ('criteria_type',)
    search_fields = ('name', 'description')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('earned_at', 'badge')
    search_fields = ('user__username', 'badge__name')
    readonly_fields = ('earned_at',)
