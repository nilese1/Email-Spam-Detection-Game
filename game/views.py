from random import random
from django.forms.widgets import static
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .models import (
    DIFFICULTY_SCORE,
    Game,
    GameEmail,
    Tutorial,
    Score,
    Email,
    User,
    DIFFICULTY_CHOICES,
)
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

    @staticmethod
    def create_game_email(game, email, level):
        game_email = GameEmail(game_id=game.id, email_id=email.id, level=level)
        game_email.save()
        return game_email

    @staticmethod
    def get_emails_with_selected_difficulty(difficulty, num_emails):
        all_emails_with_difficulty = Email.objects.filter(difficulty_level=difficulty)

        # ordering by random is slower but more readable than a for loop
        # db is small so it shouldn't matter
        random_emails_with_difficulty = all_emails_with_difficulty.order_by("?")[
            :num_emails
        ]

        return random_emails_with_difficulty

    @staticmethod
    def create_game_from_form(form, request):
        # create game object from difficulty from form
        new_game = form.save(commit=False)
        new_game.user = request.user
        new_game.level = 1
        new_game.score = 0
        new_game.start_time = timezone.now()
        new_game.end_time = None
        new_game.save()

        # add emails (GameEmails) based on difficulty
        # using 5 as a placeholder value, will define number of emails from difficulty later
        emails = GameController.get_emails_with_selected_difficulty(
            new_game.difficulty_level, 5
        )
        print(emails)
        for i, email in enumerate(emails):
            # i + 1 because i is 0-indexed and level is 1-indexed
            GameController.create_game_email(new_game, email, i + 1)
        return new_game

    @staticmethod
    def is_selection_correct(email, user_selection):
        user_selected_spam_correctly = email.spam_indicator and user_selection == "spam"
        user_selected_notspam_correctly = (
            not email.spam_indicator and user_selection == "not_spam"
        )
        return user_selected_notspam_correctly or user_selected_spam_correctly

    @staticmethod
    def get_score_from_selection(email, user_selection):
        difficulty = email.difficulty_level
        if GameController.is_selection_correct(email, user_selection):
            return DIFFICULTY_SCORE[difficulty]

        return 0


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
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            new_game = GameController.create_game_from_form(form, request)
            return redirect("game:play_game", game_id=new_game.pk)
    else:
        form = GameForm()
    return render(request, "game/start_game.html", {"form": form})


@login_required
def play_game_view(request, game_id):
    context = {}
    game = Game.objects.get(id=game_id)
    try:
        game_email = GameEmail.objects.get(game=game, level=game.level)
    except GameEmail.DoesNotExist:
        return redirect("game:game_score", game_id=game_id)
    email = game_email.email
    context["email"] = email
    context["game"] = game

    if request.method == "POST":
        action = request.POST.get("action")
        score_to_add = GameController.get_score_from_selection(email, action)
        game.level = game.level + 1
        game.score = game.score + score_to_add
        game.save()

        # byproduct of my shitty code I don't wanna fix and would rather hack it to death
        # you could ask "why not just make another function???" It's because that function would
        # shorter than this comment and I'm a fucking psycho!!!!
        is_question_correct = score_to_add > 0
        return redirect(
            "game:next_question",
            game_id=game_id,
            email_id=email.id,
            # Django has no url tag for booleans so int will have to do
            is_question_correct=int(is_question_correct),
        )

    return render(request, "game/game_detail.html", context)


# putting boolean in the url for is_question_correct is a questionable choice...
# but I don't care
@login_required()
def next_question_view(request, email_id, game_id, is_question_correct):
    context = {}
    game = Game.objects.get(id=game_id)
    email = Email.objects.get(id=email_id)

    context["game"] = game
    context["email"] = email
    context["is_question_correct"] = int(is_question_correct)

    return render(request, "game/question_result.html", context)


@login_required
def game_score_view(request, game_id):
    context = {}
    context["game"] = Game.objects.get(pk=game_id)

    return render(request, "game/game_end.html", context)
