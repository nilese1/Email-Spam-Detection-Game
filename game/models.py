from typing import final
from django.db import models
from django.contrib.auth.models import User

# The choices for what different difficulties there can be
# Other choices will throw an ValidationError if other values attempted to be saved
# in the format (actual name, human readable name)
DIFFICULTY_CHOICES = [("e", "Easy"), ("m", "Medium"), ("h", "Hard")]


@final
class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    score = models.BigIntegerField()
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True)


@final
class Email(models.Model):
    subject = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    attachment_url = models.URLField(null=True)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    spam_indicator = models.BooleanField()


@final
class GameEmail(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


@final
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    submissionDate = models.DateTimeField(auto_now=True)
