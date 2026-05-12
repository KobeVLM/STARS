from django.urls import path
from . import views
from . import admin_views
from users import views as user_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('welcome/', views.welcome, name='welcome'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
    # Admin URLs
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', admin_views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:user_id>/', admin_views.admin_user_edit, name='admin_user_edit'),
    path('admin-panel/reports/', admin_views.admin_reports, name='admin_reports'),
    path('admin-panel/reports/<int:report_id>/', admin_views.admin_report_action, name='admin_report_action'),
    path('admin-panel/badges/', admin_views.admin_badges, name='admin_badges'),
    path('admin-panel/badges/<int:badge_id>/', admin_views.admin_badge_action, name='admin_badge_action'),
    path('admin-panel/disputes/', admin_views.admin_disputes, name='admin_disputes'),
    path('admin-panel/disputes/<int:appeal_id>/', admin_views.admin_dispute_action, name='admin_dispute_action'),
    path('admin-panel/flags/', admin_views.admin_flags, name='admin_flags'),
    path('admin-panel/flags/<int:flag_id>/', admin_views.admin_flag_action, name='admin_flag_action'),
]



