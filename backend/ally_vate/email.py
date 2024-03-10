from django.core.mail import send_mail
from django.conf import settings
def send_email(subject, message, recipient_list):
    """
    Sends an email using Django's SMTP backend.

    Args:
        subject (str): The subject of the email.
        message (str): The message body of the email.
        recipient_list (list): A list of email addresses to send the email to.
    """
    # Sender email will be picked from EMAIL_HOST_USER in settings.py
    email_from=settings.EMAIL_HOST_USER
    sender_email = "shivamdave2903@gmail.com"
    send_mail(subject, message, email_from, [recipient_list])