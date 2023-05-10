from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    users_id = models.ManyToManyField(
       User, 
       related_name='chats', 
       blank=True,
       through='UserRoom'
       )
    is_group = models.BooleanField(default=False) 
    conversation = models.UUIDField(default=uuid4, editable=False, unique=True)
    primary_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.conversation}"


class ChatMessage(models.Model):
    room_id = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE
        )
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
       )
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    image = models.FileField(upload_to='chat/image/', blank=True, null=True)

    def __str__(self):
       return f"Message {self.user_id} - {self.room_id}"

 
class UserRoom(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    
    def __str__(self):
       return f"{self.user.first_name} {self.user.last_name} -> {self.room.conversation} -> {self.is_seen}"