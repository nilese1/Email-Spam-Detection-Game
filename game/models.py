from typing import final
from django.db import models
from django.contrib.auth.models import User

# The choices for what different difficulties there can be
# Other choices will throw an ValidationError if other values attempted to be saved
# in the format (actual name, human readable name)
DIFFICULTY_CHOICES = [("e", "Easy"), ("m", "Medium"), ("h", "Hard")]


@final
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    highScore = models.IntegerField(default=0)

    def update_score(self, new_score):
        """Update's the user's high score."""
        if new_score > self.highScore:
            self.highScore = new_score
            self.save()

    def play_game(self):
        """Start a game session."""
        # Placeholder comment
        pass

    def __str__(self):
        return self.username


@final
class Game(models.Model):
    level = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    score = models.BigIntegerField()
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True)

    def start(self):
        """Starts the game."""
        # Placeholder comment
        print("Game started at level: ", self.level)

    def pause(self):
        """Pauses the game."""
        # Placeholder comment
        print("Game paused.")

    def __str__(self):
        return f"Game Level {self.level}"


@final
class Tutorial(Game):
    instructions = models.TextField()

    def __str__(self):
        return f"Tutorial for Level {self.level}"


@final
class Score(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scores", null=True, blank=True
    )

    def updateScore(self, newValue):
        """Update score value and timestamp."""
        self.value = newValue
        self.timestamp = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.value} at {self.timestamp}"


@final
class Email(models.Model):
    subject = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    content = models.TextField()
    attachment_url = models.URLField(null=True)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    spam_indicator = models.BooleanField()

    def display(self):
        """Return a formatted string for display."""
        return f"Subject: {self.subject}\nFrom: {self.sender}\n\n{self.content}"

    def __str__(self):
        return self.subject


@final
class GameEmail(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


@final
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    submissionDate = models.DateTimeField(auto_now=True)
