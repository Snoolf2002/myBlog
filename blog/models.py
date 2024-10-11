from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self) -> str:
        return "{}".format(self.name)


class Blog(models.Model):
    title = models.CharField(max_length=128)
    context = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} by {self.author.last_name} {self.author.first_name}"