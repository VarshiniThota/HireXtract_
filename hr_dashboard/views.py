from django.contrib import messages
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
    scores = (
        AIScore.objects
        .filter(application__job=job)
        .select_related("application__candidate")
        .order_by("rank")
    )

    ranked_apps = [s.application for s in scores]

    unranked_apps = Application.objects.filter(
        job=job
    ).exclude(id__in=[app.id for app in ranked_apps])

    applications = ranked_apps + list(unranked_apps)

    selected_top = request.GET.get("top")
    if selected_top and selected_top.isdigit():
        applications = applications[:int(selected_top)]

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

            messages.success(request, "AI analysis completed successfully.")
            return redirect("analyze_job", job_id=job.id)

        if action == "bulk_invite":
            selected_ids = request.POST.getlist("selected_applications")

            all_applications = Application.objects.filter(job=job)

            for application in all_applications:
                candidate = application.candidate

                if str(application.id) in selected_ids:
                    send_shortlist_email(
                        candidate.email,
                        candidate.name,
                        job.title
                    )
                    application.status = "Shortlisted"
                else:
                    send_rejection_email(
                        candidate.email,
                        candidate.name,
                        job.title
                    )
                    application.status = "Rejected"

                application.save()

            messages.success(
                request,
                "Interview invites sent to selected candidates. Rejection emails sent to others."
            )
            return redirect("analyze_job", job_id=job.id)

    return render(
        request,
        "hr_dashboard/analyze_job.html",
        {
            "job": job,
            "applications": applications,
            "selected_top": selected_top,
        }
    )

