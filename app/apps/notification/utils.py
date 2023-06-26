from fcm_django.models import FCMDevice
from rest_framework.exceptions import ValidationError


def send_push_notification(title, body):
    
    devices = FCMDevice.objects.filter(active=True).distinct()

    # send notification
    devices.send_message(
        title=title,
        body=body
    )
