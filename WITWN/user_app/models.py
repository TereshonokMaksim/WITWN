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
    forbidden_recommendations = models.ManyToManyField(to = User, related_name = "accounts_norequests", blank = True)
    readers = models.ManyToManyField(to = User, related_name = "accounts_readers", blank = True)
    password = models.CharField(max_length = 200, default = "Unknown") # MADE ONLY FOR TT, DELETE FOR PRODUCTION (MAJOR SECURITY RISK)
    registered = models.BooleanField(default = False)
    birthday = models.DateField(null = True)

    def get_friends_accounts(self):
        return Account.objects.filter(**{"user__in": list(self.friends.all())})
    
    def get_requests_accounts(self):
        return Account.objects.filter(**{"user__in": list(self.requests.all())})
    
    def get_forbidden_accounts(self):
        return Account.objects.filter(**{"user__in": list(self.forbidden_recommendations.all())})

    def get_absolute_url(self):
        return reverse("confirm", args = [self.email_code])

    def __str__(self):
        return f"{self.user.username} account"