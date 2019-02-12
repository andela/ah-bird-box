from django.urls import path

# local imports
from authors.apps.profiles.views import (
    ListProfileView,
    EditUserProfileView,
    AuthorsProfileListAPIView
)

app_name = 'profile'

urlpatterns = [
    path('profiles/<str:username>', ListProfileView.as_view(), name='profile'),  # noqa
    path('profiles/edit/<str:username>', EditUserProfileView.as_view(), name='update_profile'),  # noqa
    path('profiles/', AuthorsProfileListAPIView.as_view(), name='authors_profile')  # noqa
]
