from django.urls import path
from .views import hr_dashboard, analyze_job
from .views import add_job , close_job

urlpatterns = [
    path("", hr_dashboard, name="hr_dashboard"),
    path("analyze/<int:job_id>/", analyze_job, name="analyze_job"),
    path("add-job/", add_job, name="add_job"),
    path("close-job/<int:job_id>/", close_job, name="close_job"),


]
