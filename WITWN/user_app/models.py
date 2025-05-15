from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, default = 0)
    email_code = models.CharField(max_length = 11)

    def get_absolute_url(self):
        return reverse("confirm", args = [self.email_code])

    def __str__(self):
        return self.username