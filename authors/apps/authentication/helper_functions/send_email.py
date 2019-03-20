from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import os
from decouple import config


def create_email_message(link, subject, html_template, username=None):
    email_message = render_to_string(html_template, {
        'verification_link': link,
        'title': subject,
        'username': username
    })
    return email_message


def send_email(recipient, token, request, message, subject):
    sender = os.getenv('EMAIL_SENDER')
    email_content = strip_tags(message)
    msg = EmailMultiAlternatives(
        subject, email_content, sender, to=[recipient])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_reset_password_email(recipient, token, request):
    subject = "Password Reset Request"
    password_reset_url = config("VERIFICATION_URL")
    link = "{}/update_password/{}".format(password_reset_url, token)
    message = create_email_message(link, subject, 'email_template.html')
    send_email(recipient, token, request, message, subject)
    result = {
        'message': 'Check your inbox for a link to reset your password'
    }
    return result


def send_verify_email(request, recipient_details, token):
    subject = "Verify Email for Authors Haven"
    username = recipient_details['username']
    verification_url = config("VERIFICATION_URL")
    link = "{}/verify/{}".format(verification_url, token)
    message = create_email_message(link, subject, 'email_verification.html', username) # noqa
    recipient_email = recipient_details['email']
    send_email(recipient_email, token, request, message, subject)
