from django.db import models

TAGS = [
    ('story', 'Story'),
    ('news', 'News'),
    ('event', 'Event'),
    ('programming', 'Programming'),
    ('travel', 'Travel'),
]

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=32, choices=TAGS, unique=True)

    def __str__(self) -> str:
        return "{}".format(self.name)


class Blog(models.Model):
    title = models.CharField(max_length=128)
    context = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='tags')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{}".format(self.title)