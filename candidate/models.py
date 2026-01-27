from django.db import models
from jobs.models import Job

class Candidate(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    resume = models.FileField(upload_to="resumes/")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.name} → {self.job.title}"

