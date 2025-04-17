from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from game.models import Game

# Create your views here.


def landing_view(request):
    return render(request, "landing/landing.html")


@login_required
def recent_games_view(request):
    context = {}

    number_of_games = 10
    users_games = Game.objects.filter(user=request.user).order_by("-start_time")

    context["games"] = users_games[:number_of_games]

    return render(request, "landing/recent-games.html", context)
