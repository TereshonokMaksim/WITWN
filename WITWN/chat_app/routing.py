from django.urls import path
from .consumers import ChatsConsumer, ChatStatusConsumer

ws_urlpatterns = [
    path("chat/<str:group_id>&<int:personal>", ChatsConsumer.as_asgi()),
    path("status/", ChatStatusConsumer.as_asgi())
]