from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Blog, Tag
from .serializers import BlogSerializer, BlogFilterSerializer
from .forms import BlogForm, UserRegistrationForm
from .utils import get_blog_or_404


class BlogAPIView(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all blogs with optional filters (start_date, end_date, tag, user)",
        responses={200: BlogSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY, 
                description="Filter blogs created on or after this date (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY, 
                description="Filter blogs created on or before this date (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                'tag', openapi.IN_QUERY, 
                description="Filter blogs by tag name (case-insensitive)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'user', openapi.IN_QUERY, 
                description="Filter blogs by author's username or first name or last name (case-insensitive)",
                type=openapi.TYPE_STRING,
            ),
        ],
        tags=['Blogs'],
    )
    def get_all(self, request):
        filter_serializer = BlogFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data
        blogs = Blog.objects.all()

        if 'start_date' in filters:
            blogs = blogs.filter(published_date__date__gte=filters['start_date'])
        if 'end_date' in filters:
            blogs = blogs.filter(published_date__date__lte=filters['end_date'])
        if 'tag' in filters:
            blogs = blogs.filter(tags__name__icontains=filters['tag'])
        if 'user' in filters:
            user_param = filters['user']
            blogs = blogs.filter(Q(author__first_name__icontains=user_param) | Q(author__last_name__icontains=user_param) \
                                 | Q(author__username__icontains=user_param))
        serializer = BlogSerializer(blogs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Get user's blogs with optional filters (start_date, end_date, tag)",
        responses={200: BlogSerializer(many=True)},
        tags=['Blogs'],
    )
    def get_user_blogs(self, request):
        filter_serializer = BlogFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        if not request.user.is_authenticated:
            return Response(data={"message": "You must be logged in to view your blogs."}, status=status.HTTP_401_UNAUTHORIZED)
        
        blogs = Blog.objects.filter(author=request.user)

        if 'start_date' in filters:
            blogs = blogs.filter(published_date__date__gte=filters['start_date'])
        if 'end_date' in filters:
            blogs = blogs.filter(published_date__date__lte=filters['end_date'])
        if 'tag' in filters:
            blogs = blogs.filter(tags__name__icontains=filters['tag'])

        serializer = BlogSerializer(blogs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new blog",
        request_body=BlogSerializer,
        responses={201: BlogSerializer},
        tags=['Blogs'],
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(data={"message": "You must be logged in to create a blog."}, status=status.HTTP_401_UNAUTHORIZED)
        request.data['author'] = request.user.id
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogDetailAPIView(ViewSet):
    @swagger_auto_schema(
        operation_description="Get a specific blog",
        responses={200: BlogSerializer},
        tags=['Blogs'],
    )
    def get(self, request, pk):
        blog = get_blog_or_404(pk)
        serializer = BlogSerializer(blog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Retrieve a specific blog",
        request_body=BlogSerializer,
        responses={200: BlogSerializer},
        tags=['Blogs'],
    )
    def put(self, request, pk):
        blog = get_blog_or_404(pk)
        if request.user != blog.author:
            return Response(data={"message": "You do not have permission to edit this blog."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a blog post",
        responses={204: "No Content"},
        tags=['Blogs'],
    )
    def delete(self, request, pk):
        blog = get_blog_or_404(pk)
        if request.user != blog.author:
            return Response(data={"message": "You do not have permission to delete this blog."}, status=status.HTTP_403_FORBIDDEN)

        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Django HTML Views
# Views for Templates
class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Blog.objects.all().annotate(published_month=TruncMonth('published_date')).order_by('-published_month', '-published_date')

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
        context['authors'] = User.objects.all()
        
        return context
    

class UserBlogListView(ListView):
    model = Blog
    template_name = 'user_blog_list.html'
    context_object_name = 'blogs'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Blog.objects.filter(author=self.request.user).annotate(published_month=TruncMonth('published_date')).order_by('-published_month', '-published_date')
        return queryset
    

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    permission_classes = [AllowAny]

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog-list')
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.author != request.user:
            return render(request, 'errors/permission_denied.html', status=403)
        return super().dispatch(request, *args, **kwargs)
    
# registration
def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return render(request, 'registration/register.html', {'form': form})