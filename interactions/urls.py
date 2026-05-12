from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:artwork_id>/', views.toggle_like, name='toggle_like'),
    path('comment/add/<int:artwork_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('report/<int:artwork_id>/', views.report_artwork, name='report_artwork'),
    path('comment/report/<int:comment_id>/', views.report_comment, name='report_comment'),
    path('comment/pin/<int:comment_id>/', views.pin_comment, name='pin_comment'),
    path('appeal/', views.appeal_suspension, name='appeal_suspension'),
]

