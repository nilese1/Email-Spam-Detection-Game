from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import TutorialTopic

# Create your views here.

#view for the list of topics for the user to select
class tutorialTopicList(ListView):
    template_name = "tutorial/topics.html"
    model = TutorialTopic
    context_object_name = "topics"

#view for when you click on a topic
class topicPageDetail(DetailView):
    template_name = "tutorial/topicDetail.html"
    model = TutorialTopic
    context_object_name = "topic"