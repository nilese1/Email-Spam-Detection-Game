from django.urls import path
from . import views

app_name = "leaderboard"
urlpatterns = [
    path("", views.leaderboard_view, name="leaderboard_view"),
]
