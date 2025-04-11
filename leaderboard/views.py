from django.shortcuts import render
from game.models import Game

# Create your views here.


def leaderboard_view(request):
    context = {}
    number_of_scores = 10

    top_games = Game.objects.order_by("-score")[:number_of_scores]
    context["top_games"] = top_games

    return render(request, "leaderboard/leaderboard.html", context)
