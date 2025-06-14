from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(HomeView.as_view()), name = "home"),
    path('my_publications/', login_required(MyPublicationsView.as_view()), name = 'my_publications' ),
    path('delete/<int:id>', PostDeleteView.as_view(), name = "delete_post"),
    path('delete/', PostDeleteView.as_view(), name = "delete_link"),
    path('friends/', FriendsView.as_view(), name = 'friends'),
    path("settings/", SettingsView.as_view(), name = "settings"),
    path("my_albums/", AlbumsView.as_view(), name = "my_albums"),
    path("delete_album_image/<int:id>", delete_album_image, name = "delete_image"),
    path("delete_album/<int:id>", delete_album, name = "delete_album"),
    path("change_image_visibility/<int:id>&<int:visibility>", change_visibility_image, name = "image_visibility"),
    path("change_album_visibility/<int:id>&<int:visibility>", change_visibility_album, name = "album_visibility"),
    path("create_album/", create_album, name = "create_album"),
    path("create_image/", add_image, name = "create_image"),
    path('chats/', ChatsView.as_view(), name = 'chats'),
    path("edit_main_info/", apply_user_changes, name = "edit_main_info"),
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

# Can we withstand his calamities, or it our destiny to fall?