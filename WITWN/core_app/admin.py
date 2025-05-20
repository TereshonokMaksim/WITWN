from django.contrib import admin
from .models import Tag, ImageFile, UserPost

# Register your models here.

admin.site.register([Tag, ImageFile, UserPost])