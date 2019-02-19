from django.urls import path

# local imports
from authors.apps.profiles.views import (
    ListProfileView,
    EditUserProfileView,
    AuthorsProfileListAPIView, FollowUnfollowAPIView,
    FollowerFollowingAPIView
)

app_name = 'profile'

urlpatterns = [
    path('profiles/<str:username>', ListProfileView.as_view(), name='profile'),
    path('profiles/edit/<str:username>',
         EditUserProfileView.as_view(), name='update_profile'),
    path('profiles/',
         AuthorsProfileListAPIView.as_view(), name='authors_profile'),
    path('profiles/<str:username>/follow/',
         FollowUnfollowAPIView.as_view(), name="follow"),
    path('profiles/<str:username>/following/',
         FollowerFollowingAPIView.as_view(), name="following"),
]
