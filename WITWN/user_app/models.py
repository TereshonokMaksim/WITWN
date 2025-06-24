from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



# Create your models here.

# class Account(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     avatar = models.ImageField(upload_to = "avatars/", default = "none")
#     email_code = models.CharField(max_length = 11)
#     friends = models.ManyToManyField(to = User, related_name = "accounts_friends", blank = True)
#     requests = models.ManyToManyField(to = User, related_name = "accounts_requests", blank = True)
#     forbidden_recommendations = models.ManyToManyField(to = User, related_name = "accounts_norequests", blank = True)
#     readers = models.ManyToManyField(to = User, related_name = "accounts_readers", blank = True)
#     password = models.CharField(max_length = 200, default = "Unknown") # MADE ONLY FOR TT, DELETE FOR PRODUCTION (MAJOR SECURITY RISK)
#     registered = models.BooleanField(default = False)
#     birthday = models.DateField(null = True)

#     def get_friends_accounts(self):
#         return Account.objects.filter(**{"user__in": list(self.friends.all())})
    
#     def get_requests_accounts(self):
#         return Account.objects.filter(**{"user__in": list(self.requests.all())})
    
#     def get_forbidden_accounts(self):
#         return Account.objects.filter(**{"user__in": list(self.forbidden_recommendations.all())})

#     def get_absolute_url(self):
#         return reverse("confirm", args = [self.email_code])

#     def __str__(self):
#         return f"{self.user.username} account"
    

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    signature = models.ImageField(upload_to='images/signatures', blank=True, null=True)

    def __str__(self):
        # return self.user.username
        return f"{self.user.username} | SELF ID: {self.pk} / USER ID: {self.user.pk}"
    

class Avatar(models.Model):
    image = models.ImageField(upload_to='images/avatars')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True) 
    shown = models.BooleanField(default=True) 

    def __str__(self):
        return f'Аватар для профілю {self.profile}'

        
class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_sent_request') 
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_accepted_request') 
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Зв'язок між {self.profile1} та {self.profile2}"
    
class VerificationCode(models.Model):
    username = models.CharField(max_length = 150)
    code = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Веріфікаційний код користувача {self.username}: {self.code}"

# eh, new database structure - piece of trash... or worse?