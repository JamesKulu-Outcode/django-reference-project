from rest_framework import serializers


class RegisterFCMDeviceSerializer(serializers.Serializer):
    registration_id = serializers.CharField(max_length=250)
