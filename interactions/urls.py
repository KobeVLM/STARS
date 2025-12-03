from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:artwork_id>/', views.toggle_like, name='toggle_like'),
    path('comment/add/<int:artwork_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
