from django.urls import path
from . import views

urlpatterns = [
    path('', views.explore_feed, name='feed'),
    path('upload/', views.upload_artwork, name='upload'),
    path('artwork/<int:pk>/', views.artwork_detail, name='detail'),
]
