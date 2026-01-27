from django.urls import path
from .views import job_list , apply_job

urlpatterns = [
    path("", job_list, name="job_list"),
    path("<int:job_id>/apply/", apply_job, name="apply_job"),
]
