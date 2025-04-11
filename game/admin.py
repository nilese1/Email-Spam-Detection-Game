from django.contrib import admin
from typing import final
from .models import Email, Game

# Register your models here.


@final
class EmailAdmin(admin.ModelAdmin):
    fieldsets = []

    list_display = ["subject", "difficulty_level", "spam_indicator"]


@final
class GameAdmin(admin.ModelAdmin):
    fieldsets = []

    list_display = ["user", "difficulty_level", "start_time"]


admin.site.register(Email, EmailAdmin)
admin.site.register(Game, GameAdmin)
