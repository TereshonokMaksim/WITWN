from django.db import models
from django.contrib.auth.models import User
from user_app.models import Account

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length = 255)

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
    
class ImageFile(models.Model):
    file = models.ImageField(upload_to = "posts/")
    post = models.ForeignKey(to = UserPost, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"Image from {self.post.title} post"
    
class Album(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='albums')
    title = models.CharField(max_length = 200)
    description = models.TextField(blank = True)  
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title




class AlbumImageFile(models.Model):
    album = models.ForeignKey('Album', on_delete = models.CASCADE, related_name = 'image_files')  
    file = models.ImageField(upload_to = f'albums/')

    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Image {self.pk} uploaded on {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class AlbumImage(models.Model):
    album = models.ForeignKey(Album, on_delete = models.CASCADE, related_name = 'images')  
    imagefile = models.ForeignKey(AlbumImageFile, on_delete = models.CASCADE, related_name = 'album_images')
    caption = models.CharField(max_length = 255, blank = True)

    def __str__(self):
        return f"Image {self.imagefile.pk} in album '{self.album.title}'"
