from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Blog


def get_blog_or_404(pk: int):
        return get_object_or_404(Blog, id=pk)