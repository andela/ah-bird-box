from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path(
        'notifications/',
        views.AllNotificationsAPIview.as_view(),
        name="all-notifications"
        ),
    path(
        'notifications/subscribe/',
        views.SubscribeUnsubscribeAPIView.as_view(),
        name="subscribe"
        )

]
