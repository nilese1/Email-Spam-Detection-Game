from django.urls import path
from .views import tutorialTopicList,topicPageDetail

app_name = "tutorial"
urlpatterns = [
    path("tutorial/",tutorialTopicList.as_view(), name="tutorial_list"),
    path("tutorial/<int:pk>/",topicPageDetail.as_view(),name="topic_detail")
]