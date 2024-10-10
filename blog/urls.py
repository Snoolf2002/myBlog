from django.urls import path
from .views import BlogAPIView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('api/blogs/', BlogAPIView.as_view(), name='api-blog-list'),
    path('api/blogs/<int:pk>/', BlogAPIView.as_view(), name='api-blog-detail'),
    path('', BlogListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]