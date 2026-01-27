from django.urls import path
from .views import hr_dashboard, analyze_job

urlpatterns = [
    path("", hr_dashboard, name="hr_dashboard"),
    path("analyze/<int:job_id>/", analyze_job, name="analyze_job"),
]
