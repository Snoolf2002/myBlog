from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Blog, Tag
from .serializers import BlogSerializer
from .forms import BlogForm

class BlogAPIView(APIView):
    def get(self, request: Request, pk: int = None):
        if pk is None:
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        # get single blog
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: int) -> Response:
        blog = get_object_or_404(Blog, id=pk)

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        blog = get_object_or_404(Blog, id=pk)
        blog.delete()
        return Response(data={"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Django HTML Views
class BlogListView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.tags.set(self.request.POST.getlist('tags'))
        return response


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()  # Include tags in the context
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.tags.set(self.request.POST.getlist('tags'))
        return response


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog_confirm_delete.html'
    success_url = '/'