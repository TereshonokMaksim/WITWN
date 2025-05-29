from django.urls import path
from .views import HomeView, MyPublicationsView, PostDeleteView

urlpatterns = [
    path("", HomeView.as_view(), name = "home"),
    path('my_publications/', MyPublicationsView.as_view(), name = 'my_publications' ),
    path('delete/<int:id>', PostDeleteView.as_view(), name = "delete_post"),
    path('delete/', PostDeleteView.as_view(), name = "delete_link")
]