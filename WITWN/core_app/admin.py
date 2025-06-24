from django.contrib import admin
from .models import Post, Image, Album, Tag, Link

# Register your models here.

admin.site.register([Post, Image, Album, Tag, Link])

# ...and so, he strikes us down with calamities.