from rest_framework import serializers,exceptions
from app_notification.models import Notification

class NotificationListSerializer(serializers.ModelSerializer):
    # recipient = serializers.CharField()
    # sender = serializers.CharField()
    class Meta:
        model=Notification
        fields=('id','message','recipient','sender','read',)

class NotificationDeleteSerializer(serializers.Serializer):
    notification_ids=serializers.ListField()


