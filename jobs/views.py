from django.shortcuts import get_object_or_404, render,redirect
from .models import Job
from candidate.models import Candidate, Application
from django.contrib import messages

def job_list(request):
    jobs = Job.objects.all().order_by("-created_at")
    return render(request, "jobs/job_list.html", {"jobs": jobs})

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        linkedin = request.POST.get("linkedin")
        resume = request.FILES.get("resume")

        if name and email and resume:
            candidate, created = Candidate.objects.get_or_create(
                email=email,
                defaults={
                    "name": name,
                    "linkedin_url": linkedin
                }
            )

            Application.objects.create(
                candidate=candidate,
                job=job,
                resume=resume
            )
            messages.success(
            request,
            "Your application has been submitted successfully!")

            return redirect("job_list")

    return render(request, "jobs/apply_job.html", {"job": job})