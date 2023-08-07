from rest_framework import generics
from .models import User, Post,Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404\

# from django.views.generic import UpdateView

from .serializers import UserSerializer, PostSerializer, LikeSerializer

from rest_framework import generics, permissions

from .permissions import IsOwnerOrReadOnly

from .serializers import PostSerializer

from rest_framework.generics import ListCreateAPIView

from rest_framework_simplejwt.tokens import RefreshToken

# Generate tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# User views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Post views
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Like views
class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



# CRUD ADD
@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def add_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Post added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def add_like(request):
    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Like added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CRUD READ 

def get_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    data = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "password" : user.password,
        
    }
    return JsonResponse(data)

def get_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    data = {
        "post_id": post.id,
        "title": post.title,
        "content": post.content,
        "description" : post.description,
        "ceation_date" : post.creation_date,
    }
    return JsonResponse(data)

def get_like(request, like_id):
    like = get_object_or_404(Like, pk=like_id)
    data = {
        "like_id": like.like_id,
        "user_id": like.user.user_id,
        "post_id": like.post.id,
        "timestamp": like.timestamp,
    }
    return JsonResponse(data)

# CRUD UPDATE 
@api_view(['PUT'])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'PUT':
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.save()
        return JsonResponse({'message': 'User updated successfully.'})

@api_view(['PUT'])
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'PUT':
        post.title = request.data.get('title', post.title)
        post.content = request.data.get('content', post.content)
        post.save()
        return JsonResponse({'message': 'Post updated successfully.'})

@api_view(['PUT'])
def update_like(request, pk):
    like = get_object_or_404(Like, pk=pk)

    if request.method == 'PUT':
        like.user_id = request.data.get('user', like.user_id)
        like.post_id = request.data.get('post', like.post_id)
        like.save()
        return JsonResponse({'message': 'Like updated successfully.'})
    

# CRUD DELETE


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

# POST ID



def get_all_posts(request):
    try:
        posts = Post.objects.all()
        for post in posts:
            post.likes_count = post.likes.count() 
        posts_data = [
            {
                'post_id': post.post_id,
                'title': post.title,
                'content': post.content,
                'likes_count': post.likes_count,
            }
            for post in posts
        ]

        return JsonResponse(posts_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch posts.'}, status=500)
    
# PERMISSION



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer  
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

  



class PublicPostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class PrivatePostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(owner=user)
        
        
class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


