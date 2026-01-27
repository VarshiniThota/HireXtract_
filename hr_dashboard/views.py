from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from hr_dashboard.utils import send_shortlist_email, send_rejection_email
from jobs.models import Job
from candidate.models import Application
from hr_dashboard.models import AIScore
from brainapp.screening import run_ai_screening


@login_required
def hr_dashboard(request):
    jobs = Job.objects.all()
    job_data = []

    for job in jobs:
        count = Application.objects.filter(job=job).count()
        job_data.append({
            "job": job,
            "applications": count
        })

    return render(
        request,
        "hr_dashboard/dashboard.html",
        {"job_data": job_data}
    )

@login_required
def analyze_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    applications = (
        Application.objects
        .filter(job=job)
        .select_related("candidate")
    )
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "run_ai":
            AIScore.objects.filter(application__job=job).delete()

            results = run_ai_screening(job.description, applications)

            for rank, result in enumerate(results, start=1):
                AIScore.objects.create(
                    application=result["application"],
                    score=result["score"],
                    rank=rank,
                    insights=result["insights"]
                )

            return redirect("analyze_job", job_id=job.id)
        app_id = request.POST.get("application_id")
        if action in ["invite", "reject"] and app_id:
            application = get_object_or_404(Application, id=app_id)
            candidate = application.candidate

            if action == "invite":
                send_shortlist_email(
                    candidate.email,
                    candidate.name,
                    job.title
                )
                application.status = "Shortlisted"

            elif action == "reject":
                send_rejection_email(
                    candidate.email,
                    candidate.name,
                    job.title
                )
                application.status = "Rejected"

            application.save()
            return redirect("analyze_job", job_id=job.id)
    for app in applications:
        app.ai_score = AIScore.objects.filter(application=app).first()

    return render(
        request,
        "hr_dashboard/analyze_job.html",
        {
            "job": job,
            "applications": applications,
        }
    )
