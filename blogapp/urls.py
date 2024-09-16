from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import *

urlpatterns = [
    # Blog URLs (Public Views)
    path('', views.index, name='index'),  # Home page (public access)
    path('posts/', views.post_list, name='posts-list'),  # List all posts (public access)
    path('posts/<int:post_pk>/comments/', views.comment_list, name='comment-list'),
    # List all comments on a post (public access)

    # Blog URLs (Protected Views for Logged-in Users)
    path('posts/create/', views.post_create, name='post-create'),  # Add new post (login required)
    path('posts/<int:pk>/update/', views.post_update, name='post-update'),  # Update a post (login required)
    path('posts/<int:pk>/delete/', views.post_delete, name='post-delete'),  # Delete a post (login required)
    path('posts/<int:post_pk>/comments/create/', views.comment_create, name='comment-create'),
    # Add a comment (login required)

    # Merged login_logout URLs (Authentication)
    #path('Home/', HomeView.as_view(), name='home'),  # Home view for logged-in users
     path('auth/login/', user_login, name='user_login'),
    path('register/', views.register, name='register'),
    #path('logout/', LogoutView.as_view(), name='logout'),  # Logout page
]
