from django.contrib import admin
from .models import Candidate, Application

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "linkedin_url")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "applied_at")
