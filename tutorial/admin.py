from django.contrib import admin
from .models import TutorialTopic
# Register your models here.

class tutorialAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ["topic_name, topic_content"]

admin.site.register(TutorialTopic)