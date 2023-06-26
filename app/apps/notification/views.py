from django.conf import settings
from django.utils import timezone
from fcm_django.api.rest_framework import FCMDeviceViewSet
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import RegisterFCMDeviceSerializer


class RegisterFCMDeviceView(GenericAPIView):
    """
        Register FCM device for a user
        need app-platform, Device-ID headers
    """
    queryset = FCMDevice.objects.all()
    serializer_class = RegisterFCMDeviceSerializer

    def post(self, request, *args, **kwargs):
        header_info = settings.APP_HEADER_INFORMATION
        ser = self.serializer_class(data=self.request.data)
        if not ser.is_valid():  # phone end needs in this format
            return Response({'detail': 'Invalid registration id'}, status=status.HTTP_400_BAD_REQUEST)
        app_platform = request.headers.get(
            header_info.get('APP_PLATFORM'))
        if app_platform not in ['IOS', 'ANDROID']:
            return Response({'detail': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)
        device_id = request.headers.get(
            header_info.get('DEVICE_UNIQUE_ID'))
        if not device_id:
            return Response({'detail': 'Invalid device id'}, status=status.HTTP_400_BAD_REQUEST)
        a = app_platform.lower()
        fcm_device_data = dict(
            user=self.request.user,
            type=a,
            device_id=device_id,
            registration_id=ser.data.get('registration_id'),
            active=True
        )
        if FCMDevice.objects.filter(device_id=device_id).exists():
            FCMDevice.objects.filter(device_id=device_id).update(
                date_created=timezone.now(),
                **fcm_device_data)
        else:
            FCMDevice.objects.create(
                **fcm_device_data
            )
        return Response(
            {'detail': 'Device registered'}
        )
