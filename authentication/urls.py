from django.urls import path
from .views import userRegistration, userLogin, userLogout

app_name = "authentication"
urlpatterns = [
    path("login/", userLogin.as_view(), name="login"),
    path("logout/", userLogout, name="logout"),
    path("register/", userRegistration.as_view(), name="register"),
]
