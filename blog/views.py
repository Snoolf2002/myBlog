from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Blog, Tag
from .serializers import BlogSerializer
from .forms import BlogForm

class BlogAPIView(APIView):
    def get_all_blogs(self, request: Request, pk: int = None):
        if pk is None:
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        # get single blog
        blog = get_object_or_404(Blog, id=pk)
        serializer = BlogSerializer(blog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_own_blogs(self, request: Request) -> Response:
        blogs = Blog.objects.filter(author=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        if not request.user:
            return Response(data={"message": "You must be logged in to create a blog"}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        data['author'] = request.user.id
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: int) -> Response:
        blog = get_object_or_404(Blog, id=pk)
        if blog.author != request.user:
            return Response(data={"message": "This blog does not belong to you"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        blog = get_object_or_404(Blog, id=pk)
        if blog.author != request.user:
            return Response(data={"message": "This blog does not belong to you"}, status=status.HTTP_401_UNAUTHORIZED)
        
        blog.delete()
        return Response(data={"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Django HTML Views
class BlogListView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = Blog.objects.all()

        # Filter by tag
        tag_id = self.request.GET.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        # Filter by author
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(author__id=author_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()  # List of all tags
        context['authors'] = User.objects.all()  # List of all authors
        return context


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
        form.instance.author = self.request.user
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
        blog = self.object  # Get the current blog instance
        context['tags'] = Tag.objects.all()  # All available tags
        context['selected_tags'] = blog.tags.values_list('id', flat=True)  # Currently selected tags
        return context

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            return render(request, 'errors/permission_denied.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.tags.set(self.request.POST.getlist('tags'))
        return response



class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog_confirm_delete.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            return render(request, 'errors/permission_denied.html', status=403)
        return super().dispatch(request, *args, **kwargs)