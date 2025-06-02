from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to = "avatars/", default = "avatars/default.png")
    email_code = models.CharField(max_length = 11)
    friends = models.ManyToManyField(to = User, related_name = "accounts_friends", blank = True)
    requests = models.ManyToManyField(to = User, related_name = "accounts_requests", blank = True)
    readers = models.ManyToManyField(to = User, related_name = "accounts_readers", blank = True)
    first_name = models.CharField(max_length = 100, blank = True)  
    last_name = models.CharField(max_length = 100, blank = True)   
    
    def get_friends_accounts(self):
        return Account.objects.filter(**{"user__in": list(self.friends.all())})
    
    def get_requests_accounts(self):
        return Account.objects.filter(**{"user__in": list(self.requests.all())})

    def get_absolute_url(self):
        return reverse("confirm", args = [self.email_code])
    
    def is_profile_complete(self):
        return bool(self.first_name and self.last_name and self.user.username)

    def __str__(self):
        return f"{self.user.username} account"
    