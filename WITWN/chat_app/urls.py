from django.urls import path
from .views import *


urlpatterns = [
    path("chat/", ChatsView.as_view(), name = "chats")
]