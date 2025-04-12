from django.urls import path
from .views import tutorialTopicList,topicPageDetail

app_name = "tutorial"
urlpatterns = [
    path("topics/",tutorialTopicList.as_view(), name="tutorial_list"),
    path("topics/<int:pk>/",topicPageDetail.as_view(),name="topic_detail")
]