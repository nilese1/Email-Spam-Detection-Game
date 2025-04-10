from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .models import Game, Tutorial, Score, Email, User
from django.contrib.auth.decorators import login_required
from .forms import GameForm
from django.utils import timezone


# --- GameController: encapsulates game related operations ---
class GameController:
    def __init__(self, game: Game, tutorial: Tutorial, score: Score):
        self.game = game
        self.tutorial = tutorial
        self.score = score

    def start_game(self):
        """Start the game session."""
        self.game.start()
        # You might want to render the game interface.
        return HttpResponse("Game started!")

    def end_game(self):
        """End the game session and update score."""
        self.game.pause()
        # Here we assume score update logic.
        self.score.update_score(self.score.value)
        return HttpResponse("Game ended!")

    def add_email(self, email: Email):
        """Add an email to the game session."""
        self.game.emails.add(email)
        self.game.save()
        return HttpResponse("Email added!")

    def modify_email(self, email_id: int, **kwargs):
        """Modify properties of an email in the game session."""
        try:
            email = self.game.emails.get(pk=email_id)
            for key, value in kwargs.items():
                if hasattr(email, key):
                    setattr(email, key, value)
            email.save()
            return HttpResponse("Email modified!")
        except Email.DoesNotExist:
            return HttpResponse("Email not found.", status=404)


# --- AuthController: handles login and logout operations ---
class AuthController:
    def login(self, request, user: User):
        """Log a user in."""
        # Additional custom logic can be added here.
        auth_login(request, user)
        return redirect(
            reverse("authentication:home")
        )  # Assuming 'home' is defined in your URLs.

    def logout(self, request):
        """Log a user out."""
        auth_logout(request)
        return redirect(
            reverse("authentication:login")
        )  # Assuming you have a login URL.


# --- Sample Django views using the controllers ---


def start_game_view(request, game_id, tutorial_id, score_id):
    game = get_object_or_404(Game, pk=game_id)
    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    score = get_object_or_404(Score, pk=score_id)
    controller = GameController(game, tutorial, score)
    return controller.start_game()


def end_game_view(request, game_id, tutorial_id, score_id):
    game = get_object_or_404(Game, pk=game_id)
    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    score = get_object_or_404(Score, pk=score_id)
    controller = GameController(game, tutorial, score)
    return controller.end_game()


def add_email_view(request, game_id):
    # In a real app, email details would be POSTed from a form.
    game = get_object_or_404(Game, pk=game_id)
    # For example, create a new Email instance.
    email = Email.objects.create(
        subject="New Offer",
        content="This is a spam email.",
        sender="scammer@example.com",
    )
    # In this sample, we create a dummy tutorial and score if needed (or adjust controller constructor)
    dummy_tutorial = Tutorial.objects.filter(pk=game_id).first() or game
    dummy_score = Score.objects.filter(pk=game_id).first() or Score.objects.create(
        value=0
    )
    controller = GameController(game, dummy_tutorial, dummy_score)
    return controller.add_email(email)


def modify_email_view(request, game_id, email_id):
    # In a real-world scenario, data to modify the email would come from request.POST.
    game = get_object_or_404(Game, pk=game_id)
    dummy_tutorial = Tutorial.objects.filter(pk=game_id).first() or game
    dummy_score = Score.objects.filter(pk=game_id).first() or Score.objects.create(
        value=0
    )
    controller = GameController(game, dummy_tutorial, dummy_score)
    # Example modification: update subject and content.
    kwargs = {
        "subject": "Updated Subject",
        "content": "Updated content for spam email detection game.",
    }
    return controller.modify_email(email_id, **kwargs)


@login_required
def create_game_view(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.user = request.user
            new_game.level = 1
            new_game.score = 0
            new_game.start_time = timezone.now()
            new_game.end_time = None
            new_game.save()
            # Optionally, redirect to a game interface or pass new_game to a controller
            return redirect('game:game_detail', game_id=new_game.id)
    else:
        form = GameForm()
    return render(request, 'game/start_game.html', {'form': form})
