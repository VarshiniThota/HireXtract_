from django.core.mail import send_mail
from django.conf import settings

def send_shortlist_email(candidate_email, candidate_name, job_title):
    subject = f"Interview Shortlisted – {job_title}"
    message = f"""
Dear {candidate_name},

Congratulations 🎉

You have been shortlisted for the role of {job_title}.
Our HR team will contact you shortly with next steps.

Best regards,
HireXtract HR Team
"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [candidate_email],
        fail_silently=False,
    )


def send_rejection_email(candidate_email, candidate_name, job_title):
    subject = f"Application Update – {job_title}"
    message = f"""
Dear {candidate_name},

Thank you for applying for the {job_title} role.

After careful review, we will not be moving forward at this time.
We encourage you to apply again in the future.

Best regards,
HireXtract HR Team
"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [candidate_email],
        fail_silently=False,
    )
