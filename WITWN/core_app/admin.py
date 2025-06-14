from django.contrib import admin
from .models import Tag, ImageFile, UserPost, Album, AlbumImageFile, AlbumTheme

# Register your models here.

admin.site.register([Tag, ImageFile, UserPost, AlbumTheme, Album, AlbumImageFile])

# ...and so, he strikes us down with calamities.