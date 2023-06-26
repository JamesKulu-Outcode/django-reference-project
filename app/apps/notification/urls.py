from django.urls import path

from .views import RegisterFCMDeviceView

# router = DefaultRouter()
# router.register(r'devices', FCMDeviceViewSet)

urlpatterns = [
    # url(r'^docs/', include_docs_urls(title='FCM django web demo')),
    # url(r'^', include(router.urls)),
    path('device/register/', RegisterFCMDeviceView.as_view(), name='create_fcm_device'),

]
