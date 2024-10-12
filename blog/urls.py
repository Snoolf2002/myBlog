from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
                    BlogAPIView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, 
                    BlogDeleteView, UserBlogListView, register, BlogDetailAPIView
                    )   

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # For getting all blogs and creating a new blog
    path('api/blogs/', BlogAPIView.as_view({'get': 'get_all', 'post': 'post'}), name='api-blogs'), 
    path('api/blogs/<int:pk>/', BlogDetailAPIView.as_view({'get': 'get', 'put': 'put', 'delete': 'delete'}), name='api-blog-detail'),  
    
    path('register/', register, name='register'),
    path('', BlogListView.as_view(), name='blog-list'),
    path('my-blogs/', UserBlogListView.as_view(), name='user-blog-list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog-edit'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]