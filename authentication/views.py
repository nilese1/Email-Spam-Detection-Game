from django.views.generic.edit import FormView
from .forms import UserSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


# Create your views here.
# handles the account creation page
class userRegistration(FormView):
    template_name = "registration.html"
    form_class = UserSignupForm
    success_url = reverse_lazy("authentication:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# handles the login page
class userLogin(LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("game")

    def form_valid(self, form):
        return super().form_valid(form)


class userLogout(LogoutView):
    template_name = "logout.html"

