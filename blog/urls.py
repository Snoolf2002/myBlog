from django.urls import path
from .views import BlogAPIView

urlpatterns = [
    path('blogs/', BlogAPIView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogAPIView.as_view(), name='blog-detail'),  
]