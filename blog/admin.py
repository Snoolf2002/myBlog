from django.contrib import admin
from .models import Tag, Blog
# Register your models here.

admin.site.register([Tag, Blog])