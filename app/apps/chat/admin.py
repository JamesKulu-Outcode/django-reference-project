from django.contrib import admin

# Register your models here.

from .models import (
    ChatMessage, 
    ChatRoom,
    UserRoom
)

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        'room_id', 
        'user_id', 
        'message', 
        'created_at')

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'conversation', 
        'created_at')

admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(UserRoom)