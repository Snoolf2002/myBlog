from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
                    BlogAPIView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, 
                    BlogDeleteView, UserBlogListView, register
                    )   

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/blogs/', BlogAPIView.as_view(), name='api-blog-list'),
    path('api/blogs/<int:pk>/', BlogAPIView.as_view(), name='api-blog-detail'),

    path('register/', register, name='register'),
    path('', BlogListView.as_view(), name='blog-list'),
    path('my-blogs/', UserBlogListView.as_view(), name='user-blog-list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]