from rest_framework import serializers

from notifications.models import Notification

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class SubscribeUnsubscribeSerializer(serializers.Serializer):
    """
    serializer class for unsubscribing from email notifications
    """
    email = serializers.BooleanField(required=True)
    app = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('email_notification_subscription',
                  'app_notification_subscription')


class ActorTargetField(serializers.RelatedField):
    """
    class to represent an actor/target
    """

    def to_representation(self, value):
        actor_type = None
        data = []
        if isinstance(value, Article):
            actor_type = "article"
            data = value.slug

        elif isinstance(value, User):
            actor_type = "user"
            data = value.username

        return {"type": actor_type, "data": data}

    def to_internal_value(self, data):
        return Notification(data)


class NotificationSerializer(serializers.ModelSerializer):
    """
    serializer class for notification objects
    """
    actor = ActorTargetField(read_only=True)
    target = ActorTargetField(read_only=True)

    class Meta:
        model = Notification
        fields = (
            'id',
            'actor',
            'verb',
            'target',
            'level',
            'unread',
            'timestamp',
            'description',
            'emailed')
