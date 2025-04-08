from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#creates a custom sign up form that includes user email.
class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]