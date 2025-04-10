from django.urls import path
from . import views

app_name = "game"
urlpatterns = [
    path("create/", views.create_game_view, name="create_game"),
    path(
        "<int:game_id>/tutorial/<int:tutorial_id>/score/<int:score_id>/start/",
        views.start_game_view,
        name="start_game",
    ),
    path(
        "<int:game_id>/tutorial/<int:tutorial_id>/score/<int:score_id>/end/",
        views.end_game_view,
        name="end_game",
    ),
    path("<int:game_id>/email/add/", views.add_email_view, name="add_email"),
    path(
        "<int:game_id>/email/<int:email_id>/modify/",
        views.modify_email_view,
        name="modify_email",
    ),
]
