from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'authors.apps.profiles'

    def ready(self):
        from authors.apps.usernotifications import handlers  # noqa