from django.urls import path
from .consumers import UserStatusConsumer


ws_urlpatterns = [
    path("user_status/", UserStatusConsumer.as_asgi())
]