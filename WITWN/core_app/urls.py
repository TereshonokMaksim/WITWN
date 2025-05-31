from django.urls import path
from .views import HomeView, MyPublicationsView, PostDeleteView, FriendsView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(HomeView.as_view()), name = "home"),
    path('my_publications/', login_required(MyPublicationsView.as_view()), name = 'my_publications' ),
    path('delete/<int:id>', PostDeleteView.as_view(), name = "delete_post"),
    path('delete/', PostDeleteView.as_view(), name = "delete_link"),
    path('friends/', FriendsView.as_view(), name = 'friends')
]