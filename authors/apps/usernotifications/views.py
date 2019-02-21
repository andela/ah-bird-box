from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView
    )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import NotificationSerializer, SubscribeUnsubscribeSerializer
from authors.apps.authentication.models import User


class NotificationApiView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notifications = self.notifications(request)
        serializer = self.serializer_class(
            notifications, many=True, context={'request': request}
        )

        return Response(
            {"count": notifications.count(), "notifications": serializer.data}
        )

    def notifications(self, request):
        # this method will be overridden by the following methods
        pass


class AllNotificationsAPIview(NotificationApiView):
    """
    list all user's notifications
    """
    def notifications(self, request):
        request.user.notifications.mark_as_sent()
        return request.user.notifications.active()


class SubscribeUnsubscribeAPIView(UpdateAPIView):
    """
    lets users to subscribe to notifications.
    """
    perission_classes = [IsAuthenticated]
    serializer_class = SubscribeUnsubscribeSerializer

    def post(self, request):
        user = get_object_or_404(User, email=request.user.email)
        setting_data = request.data
        serializer = self.serializer_class(
            data=setting_data, context={'request': request})
        if serializer.is_valid():
            if 'email' in setting_data:
                email_status = setting_data['email']
                user.email_notification_subscription = setting_data['email']
            if 'app' in setting_data:
                app_status = setting_data['app']
                user.app_notification_subscription = setting_data['app']

            user.save()
        message = {
            "message": f"You have successfully set email to {email_status} and app to {app_status}",  # noqa E501
            "data": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)
