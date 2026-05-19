from django.urls import path
from standup import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/', views.post_standup, name='post_standup'),
    path('feed/partial/', views.feed_partial, name='feed_partial'),
    path('register/', views.register, name='register'),
]
