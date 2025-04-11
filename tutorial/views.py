from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import TutorialTopic

# Create your views here.
class tutorialTopicList(ListView):
    template_name = "tutorial/topics.html"
    model = TutorialTopic

class topicPageDetail(DetailView):
    template_name = "tutorial/topicDetail.html"