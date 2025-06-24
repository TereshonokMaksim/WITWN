from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(HomeView.as_view()), name = "home"),
    path('my_publications/', login_required(MyPublicationsView.as_view()), name = 'my_publications' ),
    path('delete/<int:id>', PostDeleteView.as_view(), name = "delete_post"),
    path('delete/', PostDeleteView.as_view(), name = "delete_link"),
    path("settings/", SettingsView.as_view(), name = "settings"),
    path("my_albums/", AlbumsView.as_view(), name = "my_albums"),
    path("delete_album_image/<int:id>", delete_album_image, name = "delete_image"),
    path("delete_album/<int:id>", delete_album, name = "delete_album"),
    path("change_image_visibility/<int:id>&<int:visibility>", change_visibility_image, name = "image_visibility"),
    path("change_album_visibility/<int:id>&<int:visibility>", change_visibility_album, name = "album_visibility"),
    path("create_album/", create_album, name = "create_album"),
    path("create_image/", add_image, name = "create_image"),
    path("edit_main_info/", apply_user_changes, name = "edit_main_info"),
    path("change_password_link/", change_password, name = "change_password_link")
]

# Can we withstand his calamities, or is it our destiny to fall?