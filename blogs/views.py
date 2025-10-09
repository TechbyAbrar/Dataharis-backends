# from rest_framework import viewsets, permissions, status, generics
# from rest_framework.response import Response
# from rest_framework.exceptions import PermissionDenied
# from .models import Blog, MsPost
# from .serializers import BlogSerializer, MsPostSerializer
# from .permissions import IsOwnerOrSuperUser, IsSuperUserOrReadOnly
# from rest_framework.permissions import IsAuthenticated

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

# # @method_decorator(cache_page(60 * 15), name='dispatch')
# class BlogListCreateView(generics.ListCreateAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     permission_classes = [IsOwnerOrSuperUser]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     permission_classes = [IsOwnerOrSuperUser, IsOwnerOrSuperUser]

# # @method_decorator(cache_page(60 * 15), name='dispatch')
# class MsPostListCreateAPIView(generics.ListCreateAPIView):
#     queryset = MsPost.objects.all().order_by('-created_at')
#     serializer_class = MsPostSerializer
#     permission_classes = [IsSuperUserOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class MsPostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MsPost.objects.all()
#     serializer_class = MsPostSerializer
#     permission_classes = [IsSuperUserOrReadOnly]


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Blog, MsPost, MsVideo
from .serializers import BlogSerializer, MsPostSerializer, MsVideoSerializer
from .permissions import IsOwnerOrSuperUser, IsSuperUserOrReadOnly
from .base import BaseAPIView


class BlogListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrSuperUser]


class MsPostListCreateAPIView(BaseAPIView, generics.ListCreateAPIView):
    queryset = MsPost.objects.all().order_by('-created_at')
    serializer_class = MsPostSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MsPostRetrieveUpdateDestroyAPIView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = MsPost.objects.all()
    serializer_class = MsPostSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class MsVideoListCreateAPIView(BaseAPIView, generics.ListCreateAPIView):
    queryset = MsVideo.objects.all().order_by('-created_at')
    serializer_class = MsVideoSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class MsVideoRetrieveUpdateDestroyAPIView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = MsVideo.objects.all()
    serializer_class = MsVideoSerializer
    permission_classes = [IsSuperUserOrReadOnly]