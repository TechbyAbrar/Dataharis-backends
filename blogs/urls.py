from django.urls import path
from .views import BlogListCreateView, BlogDetailView, MsPostListCreateAPIView, MsPostRetrieveUpdateDestroyAPIView, MsVideoListCreateAPIView, MsVideoRetrieveUpdateDestroyAPIView



urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    # path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('ms-posts/', MsPostListCreateAPIView.as_view(), name='post-list-create'),
    path('ms-posts/<int:pk>/', MsPostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    # admin video embed system
    path('ms-videos/', MsVideoListCreateAPIView.as_view(), name='video-list-create'),
    path('ms-videos/<int:pk>/', MsVideoRetrieveUpdateDestroyAPIView.as_view(), name='video-detail'),
]


# api/blogs/v1/ms-videos/
# api/blogs/v1/ms-videos/<int:pk>/