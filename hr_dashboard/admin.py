from django.contrib import admin
from .models import AIScore

@admin.register(AIScore)
class AIScoreAdmin(admin.ModelAdmin):
    list_display = ("application", "score", "rank", "analyzed_at")

