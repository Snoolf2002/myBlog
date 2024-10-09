from django.db import models

TAGS = [
    ('ST', 'story'),
    ('PR', 'programming'),
    ('L', 'life'),
    ('IN', 'internships'),
    ('MAANG', 'companies')
]

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=32, choices=TAGS, unique=True)


class Blog(models.Model):
    title = models.CharField(max_length=128)
    context = models.TextField()
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)