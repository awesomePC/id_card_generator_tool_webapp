from time import sleep

from celery import shared_task
from django.core.mail import send_mail

#Here you can create various task functions
@shared_task()
def sample_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation that freezes Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )
