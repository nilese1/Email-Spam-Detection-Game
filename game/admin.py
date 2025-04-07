from django.contrib import admin
from typing import final
from .models import Email

# Register your models here.

@final
class EmailAdmin(admin.ModelAdmin):
    fieldsets = []

    list_display = ["subject", "difficulty_level", "spam_indicator"]


admin.site.register(Email, EmailAdmin)
