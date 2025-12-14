from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer


User = get_user_model()

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('comments__author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | 
                models.Q(content__icontains=search)
            )
        return queryset.select_related('author').prefetch_related('comments__author')

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = Comment.objects.all().filter(post=post).select_related('author')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('post__author', 'author')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.all().select_related('post__author', 'author')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # Get users that current user follows
    following_users = request.user.followers.all()
    # Get posts from followed users + own posts
    feed_posts = Post.objects.filter(
        author__in=following_users
    ).select_related('author').prefetch_related('comments__author').order_by('-created_at')
    
    serializer = PostSerializer(feed_posts, many=True)
    return Response(serializer.data)