from django.urls import path
from .views import BlogAPIView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('api/blogs/', BlogAPIView.as_view(), name='api-blog-list'),
    path('api/blogs/<int:pk>/', BlogAPIView.as_view(), name='api-blog-detail'),
    path('', BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]