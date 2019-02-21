"""
app config module
"""

from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'authors.apps.comments'

    def ready(self):
        from authors.apps.usernotifications import handlers  # noqa
