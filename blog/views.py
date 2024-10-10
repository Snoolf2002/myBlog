from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .models import Blog
from .serializers import BlogSerializer

class BlogAPIView(APIView):
    def get(self, request: Request, pk: int = None) -> Response:
        if pk is None:
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        # get single blog
        blog = Blog.objects.filter(id=pk).first()
        if blog is None:
            return Response(data={"error": "Blog Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, pk: int) -> Response:
        blog = Blog.objects.filter(id=pk).first()
        if blog is None:
            return Response(data={"error": "Blog Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        blog = Blog.objects.filter(id=pk).first()
        if blog is None:
            return Response(data={"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response(data={"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
