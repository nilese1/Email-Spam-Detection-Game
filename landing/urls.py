from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "landing"
urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("recent-games", views.recent_games_view, name="recent_games"),
]
