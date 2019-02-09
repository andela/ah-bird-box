from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import os


def send_email(recipient, token, request):
    subject = "Password Reset Request"
    sender = os.getenv('EMAIL_SENDER')
    host_url = get_current_site(request)
    reset_link = "http://" + host_url.domain + \
        '/api/users/update_password/' + token
    email_message = render_to_string('email_template.html', {
        'verification_link': reset_link,
        'title': subject
    })
    email_content = strip_tags(email_message)
    msg = EmailMultiAlternatives(
        subject, email_content, sender, to=[recipient])
    msg.attach_alternative(email_message, "text/html")
    msg.send()
    result = {
        'message': 'Check your inbox for a link to reset your password'
    }
    return result
