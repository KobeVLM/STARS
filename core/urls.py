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
]



