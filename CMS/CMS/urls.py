"""
URL configuration for CMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cmsapp.views import UserListCreateView, UserRetrieveUpdateDestroyView, PostListCreateView, PostRetrieveUpdateDestroyView, LikeListCreateView, LikeRetrieveUpdateDestroyView
from cmsapp import views
from cmsapp.views import update_user, update_post, update_like
from cmsapp.views import get_all_posts

from cmsapp.views import PublicPostListView, PrivatePostListView
from cmsapp.views import PostListCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    #  User model
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users1/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    #  Post model
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts1/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),

    #  Like model
    path('api/likes/', LikeListCreateView.as_view(), name='post-list-create'),
    path('api/likes1/<int:pk>/', LikeRetrieveUpdateDestroyView.as_view(), name='like-retrieve-update-destroy'),

    # CRUD ADD

    path('api/users', views.add_user, name='add_user'),
    path('api/posts', views.add_post, name='add_post'),
    path('api/likes', views.add_like, name='add_like'),


    # CRUD READ 
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('posts/<int:post_id>/', views.get_post, name='get_post'),
    path('likes/<int:like_id>/', views.get_like, name='get_like'),

    # CRUD UPDATE

    path('update/user/', update_user, name='user-update'),
    path('update/post/', update_post, name='post-update'),
    path('update/like/', update_like, name='like-update'),

    # CRUD DELETE

    path('api/user/delete/', views.UserDeleteView.as_view(), name='api-delete-user'),
    path('api/post/delete/', views.PostDeleteView.as_view(), name='api-delete-post'),
    path('api/like/delete/', views.LikeDeleteView.as_view(), name='api-delete-like'),

    # POST ID 

     path('api/posts.id/', get_all_posts, name='get_all_posts'),


     path('public-posts/', PublicPostListView.as_view(), name='public-post-list'),
     path('private-posts/', PrivatePostListView.as_view(), name='private-post-list'),

     path('api/posts.create/', PostListCreateAPIView.as_view(), name='post-list-create'),
]




