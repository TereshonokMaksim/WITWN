from django.db import models
from django.contrib.auth.models import User
from user_app.models import Account

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length = 255)
    color = models.CharField(max_length = 9)

    def __str__(self):
        return self.name

class UserPost(models.Model):
    author = models.ForeignKey(to = Account, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    theme = models.CharField(max_length = 511)
    tags = models.ManyToManyField(to = Tag)
    text = models.TextField()
    links = models.TextField(null=True, default = "") # sep between links: " " (forbidden in urls)
    watched_by = models.ManyToManyField(to = Account, related_name = "users_watched")
    liked_by = models.ManyToManyField(to = Account, related_name = "users_liked")
    # images = models.FieldFile(upload_to = "posts/")
    # Remember: To get number of likes or watches just use len(UserPost.wached_by)

    def __str__(self):
        return f"{self.title} by {self.author.user.username}"
    
class ImageFile(models.Model):
    file = models.ImageField(upload_to = "posts/")
    post = models.ForeignKey(to = UserPost, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"Image from {self.post.title} post"