from .views import *
from django.urls import path



urlpatterns = [
            path('friends/', FriendsView.as_view(), name = 'friends'),
            path("all_friends/", AllFriendsView.as_view(), name = "all_friends"),
            path("all_requests/", AllRequestsView.as_view(), name = "all_requests"),
            path("all_recomendations/", AllRecomendationsView.as_view(), name = "all_recomendations"),
            path("add_friend/<int:id>", add_friend, name = "add_friend"),
            path("remove_friend/<int:id>", remove_friend, name = "remove_friend"),
            path("deny_request/<int:id>", deny_request, name = "deny_request"),
            path("send_request/<int:id>", send_request, name = "send_request"),
            path("delete_recomendation/<int:id>", delete_recomendation, name = "delete_recomendation"),
            path("user_page/<int:id>", UserView.as_view(), name = "user_page")
            ]