from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer


class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'


class PostDeletelAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer


	def perform_create(self, serializer):
		serializer.save(author=self.request.user)
	