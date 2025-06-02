from django.urls import path
from .views import HomeView, MyPublicationsView, PostDeleteView, FriendsView,  AcceptFriendRequestView, DeclineFriendRequestView, SendFriendRequestView, RemoveFriendView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(HomeView.as_view()), name = "home"),
    path('my_publications/', login_required(MyPublicationsView.as_view()), name = 'my_publications' ),
    path('delete/<int:id>', PostDeleteView.as_view(), name = "delete_post"),
    path('delete/', PostDeleteView.as_view(), name = "delete_link"),
    path('friends/', login_required(FriendsView.as_view()), name = 'friends'),
    path('friends/accept/<int:user_id>/', login_required(AcceptFriendRequestView.as_view()), name = 'accept_friend'),
    path('friends/decline/<int:user_id>/', login_required(DeclineFriendRequestView.as_view()), name = 'decline_friend'),
    path('friends/remove/<int:user_id>/', login_required(RemoveFriendView.as_view()), name = 'remove_friend'),
    path('recommendations/send_request/<int:user_id>/', login_required(SendFriendRequestView.as_view()), name = 'send_friend_request'),
]