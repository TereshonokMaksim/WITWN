from django.urls import path
from .views import *


urlpatterns = [
    path("reg/", RegView.as_view(), name = "reg"),
    path("login/", LoginView.as_view(), name = "login"),
    path("", HomeView.as_view(), name = "home"),
    path("reg2/", Reg2View.as_view(), name = "reg2"),
    path("registration_success/", ConfirmationView.as_view(), name = "success"),
    path("logout/", logout_user, name = "logout")
]