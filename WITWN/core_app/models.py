# from django.db import models
# from django.contrib.auth.models import User
# from user_app.models import Account
# from django.contrib.contenttypes.models import ContentType 

# # Create your models here.

# class Tag(models.Model):
#     name = models.CharField(max_length = 255)
#     standart = models.BooleanField(default = False)

#     def __str__(self):
#         return f"{self.name} Tag"

# class UserPost(models.Model):
#     author = models.ForeignKey(to = Account, on_delete = models.CASCADE)
#     title = models.CharField(max_length = 255)
#     theme = models.CharField(max_length = 511)
#     tags = models.ManyToManyField(to = Tag)
#     text = models.TextField()
#     links = models.TextField(null=True, default = "") # sep between links: " " (forbidden in urls)
#     watched_by = models.ManyToManyField(to = Account, related_name = "users_watched")
#     liked_by = models.ManyToManyField(to = Account, related_name = "users_liked")
#     # Remember: To get number of likes or watches just use len(UserPost.wached_by)

#     def __str__(self):
#         return f"{self.title} by {self.author.user.username}"
    
# class AlbumTheme(models.Model):
#     name = models.CharField(max_length = 255)

#     def __str__(self):
#         return self.name

# class Album(models.Model):
#     author = models.ForeignKey(to = Account, on_delete = models.CASCADE)
#     name = models.CharField(max_length = 255)
#     theme = models.ForeignKey(to = AlbumTheme, on_delete = models.SET_NULL, null = True)
#     year = models.IntegerField(blank = True, null = True)
#     public = models.BooleanField(default = True)
#     necessary = models.BooleanField(default = False)
#     # Если правда, то его невозможно удалить со стороны пользователя    
# #
#     def __str__(self):
#         return f'"{self.name}" album from {self.author}'

# class ImageFile(models.Model):
#     file = models.ImageField(upload_to = "posts/")
#     post = models.ForeignKey(to = UserPost, on_delete = models.CASCADE)
    
#     def __str__(self):
#         return f"Image from {self.post.title} post"
    
# class AlbumImageFile(models.Model):
#     file = models.ImageField(upload_to = "albums/")
#     album = models.ForeignKey(to = Album, on_delete = models.CASCADE)
#     public = models.BooleanField(default = True)
    
#     def __str__(self):
#         return f"Image from {self.album.name} album"
    
# # What if we are wrong here?

from django.db import models
from user_app.models import Profile


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=4096)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    images = models.ManyToManyField('Image', blank=True, related_name='posts_authored')
    views = models.ManyToManyField(Profile, blank=True, related_name='posts_viewed')
    likes = models.ManyToManyField(Profile, blank=True, related_name='posts_liked')
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    filename = models.CharField(max_length=150)
    file = models.ImageField(upload_to='images/posts')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
    

class Album(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_image = models.ImageField(upload_to='images/album_previews', null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    shown = models.BooleanField(default=True)
    topic = models.ForeignKey('Tag', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Link(models.Model):
    url = models.URLField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Посилання для поста "{self.post}"'
    
# Im in tears because of how bad this db structure is