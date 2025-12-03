from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('welcome/', views.welcome, name='welcome'),
    
    # Admin URLs
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', admin_views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:user_id>/', admin_views.admin_user_edit, name='admin_user_edit'),
]
