from django.conf import settings
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.urls import reverse
from notifications.signals import notify
from notifications.models import Notification
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from authors.apps.comments.models import Comments
from . import action as verbs


def email_notification_handler(sender, instance, created, **kwargs):
    """
    notification handler for emails.
    """
    user = instance.recipient
    recipient = User.objects.get(email=user)
    if recipient.email_notification_subscription is False:
        return
    description = instance.description
    opt_out_link = f'{settings.DOMAIN}/api/notifications/subscribe/'
    try:
        resource_url = instance.data['resource_url']
    except TypeError:
        resource_url = f"{settings.DOMAIN}/api/articles"

    html_content = render_to_string('notification_template.html', context={
        "opt_out_link": opt_out_link,
        "username": recipient.username,
        "description": description,
        "resource_url": resource_url
    })
    send_mail(
        "User Notification",
        '',
        'ahbirdbox03@gmail.com',
        [recipient.email],
        html_message=html_content)


def article_handler(sender, instance, created, **kwargs):
    """
    notification handler for articles
    """
    article_author = instance.author
    followers = article_author.followers.all()
    subscribed_users = [user for user in followers if user.app_notification_subscription is True]  # noqa

    if not subscribed_users:
        return
    for user in subscribed_users:

        url = reverse(
            "articles:article-details", args=[instance.slug])
        url = f"{settings.DOMAIN}{url}"
        notify.send(
            article_author,
            recipient=user,
            description="{} posted an article on {}".format(
                article_author.username,
                instance.created_at.strftime('%d-%B-%Y %H:%M')),
            verb=verbs.ARTICLE_CREATION,
            action_object=instance,
            resource_url=url
            )


def comment_handler(sender, instance, created, **kwargs):
    """
    notification handler for comments
    """
    recipients = []
    if instance.parent and instance.parent.author != instance.author:
        # comment is part of a thread
        parent_comment_author = instance.parent.author
        recipients.append(parent_comment_author)
    comment_author = instance.author
    article = instance.article
    desc_string = "{} posted a comment to {} on {}"
    article_author = article.author
    if article_author.id != comment_author.id:
        recipients.append(article_author)
    url = reverse(
            "articles:article-details", args=[article.slug])
    resource_url = f"{settings.DOMAIN}{url}"

    notify.send(comment_author,
                recipient=recipients,
                description=desc_string.format(comment_author.username,
                                               article or instance,
                                               instance.created_at.strftime('%d-%B-%Y %H:%M')),  # noqa
                verb=verbs.COMMENT_CREATED,
                target=article or instance,
                action_object=instance,
                resource_url=resource_url)


post_save.connect(email_notification_handler, sender=Notification)
post_save.connect(article_handler, sender=Article, weak=False)
post_save.connect(comment_handler, sender=Comments, weak=False)
