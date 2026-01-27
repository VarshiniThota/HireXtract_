from django.db import models
from candidate.models import Application

class AIScore(models.Model):
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="ai_score"
    )
    score = models.FloatField()
    rank = models.IntegerField()
    insights = models.TextField(blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.candidate.name} - {self.score}%"

