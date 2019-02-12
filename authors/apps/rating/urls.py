from django.urls import path

from .views import (
    RatingsRetrieveAPIView
)

app_name = 'rating'

urlpatterns = [
    path('', RatingsRetrieveAPIView.as_view(), name='all_ratings'),
]
