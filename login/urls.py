from django.urls import path
from .views import userRegistration, userLogin, userLogout

urlpatterns = [
    path('login/', userLogin.as_view(), name='login'),
    path('logout/', userLogout.as_view(), name='logout'),
    path('register/', userRegistration.as_view(), name='register')
]