from django.contrib import admin
from .models import Profile, VerificationCode, Friendship, Avatar


# Register your models here.

admin.site.register([Profile, VerificationCode, Friendship, Avatar])