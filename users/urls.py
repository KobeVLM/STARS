from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),
    path('settings/', views.account_settings, name='account_settings'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
