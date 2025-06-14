from django.db import models
from django.contrib.auth.models import User
from user_app.models import Account
from django.contrib.contenttypes.models import ContentType 

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length = 255)
    standart = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} Tag"

class UserPost(models.Model):
    author = models.ForeignKey(to = Account, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    theme = models.CharField(max_length = 511)
    tags = models.ManyToManyField(to = Tag)
    text = models.TextField()
    links = models.TextField(null=True, default = "") # sep between links: " " (forbidden in urls)
    watched_by = models.ManyToManyField(to = Account, related_name = "users_watched")
    liked_by = models.ManyToManyField(to = Account, related_name = "users_liked")
    # Remember: To get number of likes or watches just use len(UserPost.wached_by)

    def __str__(self):
        return f"{self.title} by {self.author.user.username}"
    
class AlbumTheme(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class Album(models.Model):
    author = models.ForeignKey(to = Account, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
    theme = models.ForeignKey(to = AlbumTheme, on_delete = models.SET_NULL, null = True)
    year = models.IntegerField(blank = True, null = True)
    public = models.BooleanField(default = True)
    necessary = models.BooleanField(default = False)
    # Если правда, то его невозможно удалить со стороны пользователя    

    def __str__(self):
        return f'"{self.name}" album from {self.author}'

class ImageFile(models.Model):
    file = models.ImageField(upload_to = "posts/")
    post = models.ForeignKey(to = UserPost, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"Image from {self.post.title} post"
    
class AlbumImageFile(models.Model):
    file = models.ImageField(upload_to = "albums/")
    album = models.ForeignKey(to = Album, on_delete = models.CASCADE)
    public = models.BooleanField(default = True)
    
    def __str__(self):
        return f"Image from {self.album.name} album"
    
# What if we are wrong here?