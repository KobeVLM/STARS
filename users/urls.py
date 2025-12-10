from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),
    path('settings/', views.account_settings, name='account_settings'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]


