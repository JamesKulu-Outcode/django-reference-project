from django.urls import path
from .views import (
    ChatRoomDetailView,
    ChatRoomView,
    ChatReadUpdateView,
    PrivateConversationCreate
)

urlpatterns = [
    path('<str:conversation>/', ChatRoomDetailView.as_view(), name="chat-detail"),
    path('', ChatRoomView.as_view(), name="chat-room-list"),
    path('read/messages/', ChatReadUpdateView.as_view(), name="chat-read-view"),
    path('private/create/', PrivateConversationCreate.as_view(), name="private-conversation-create"),
]