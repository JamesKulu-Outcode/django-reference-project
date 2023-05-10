import json
#from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer# import the logging library
import logging
import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

# from api.models import BaseUser as User
User =  get_user_model()

from .models import (
    ChatMessage, 
    ChatRoom,
    UserRoom
)

# from api.models import Organization

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.room_group_name = f"chat_{self.room_name}"

        # # Join room group
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.user = self.scope["user"]
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()
        # Leave room group
        # await self.channel_layer.group_discard(
        #     self.room_group_name, 
        #     self.channel_name
        #     )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json["event_type"]

        # self.conversation = conversation
        # self.conversation_group_name = f"chat_{conversation}"
        self.conversation_group_name = f"chat_{self.user.id}"
        # self.organization_id = self.user.organization.id if self.user.organization else None

        # Join room group
        if event_type == 'join_room':
            # flag = await self.check_user_in_conversation(conversation, organization_id)
            # if flag:
            await self.channel_layer.group_add(self.conversation_group_name, self.channel_name)
            await self.channel_layer.group_send(
                self.conversation_group_name, 
                {
                    "type": event_type, 
                    "group_joined": True 
                }
            )

        elif event_type == 'chat_message':
            conversation = text_data_json["conversation"]
            message = text_data_json["message"]
            user_id = self.user.id

            flag = await self.check_user_in_conversation(conversation)
            if flag:
                chat_message = await self.save_message(user_id, conversation, message)
                users = await self.users_list(conversation)
                # Send message to room group            
                for user in users:
                    await self.channel_layer.group_send(
                        f'chat_{user}',
                        {
                            "type": "chat_message", 
                            "message": message,
                            "user_id": user_id,
                            "conversation": conversation,
                            "unread_count": await self.get_unread_count(user),
                            "message_obj": {
                                "id": chat_message.id if chat_message else None,
                                "message": chat_message.message if chat_message else None,
                                "sender": {
                                    "id": chat_message.user_id.id if chat_message else None,
                                    "full_name": f'{chat_message.user_id.first_name} {chat_message.user_id.last_name}' if chat_message else None
                                },
                                "created_at": chat_message.created_at.isoformat().split('+')[0] + 'Z' if chat_message else None
                            }
                        }
                    )
        elif event_type == 'ping':
            await self.channel_layer.group_add(self.conversation_group_name, self.channel_name)
            await self.channel_layer.group_send(
                self.conversation_group_name, 
                {
                    "type": "ping"
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        conversation = event["conversation"]
        message_obj = event["message_obj"]
        unread_count = event["unread_count"]
        
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "type": "chat_message",
                "conversation": conversation,
                "unread_count": unread_count,
                "data": {
                    "id": message_obj['id'],
                    "message": message_obj['message'],
                    "created_at": message_obj['created_at'],
                    "sender": message_obj['sender'],
                }
            }))
    
    async def join_room(self, event):
        group_joined = event["group_joined"]
        
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "event_type": event['type'],
                "group_joined": group_joined,
            }))
    
    async def ping(self, event):
        # Send message to WebSocket
        await self.send("pong")
    
    @database_sync_to_async
    def save_message(self, user_id, conversation, message):
        
        try:
            user = User.objects.get(id=user_id)
            room = ChatRoom.objects.get(conversation=conversation)
            
            # return await self.close(code=4000)
            chat_message = ChatMessage.objects.create(
                user_id=user,
                room_id=room, 
                message=message,
            )
            
            # is_seen set to true for user who sent the message
            loggedin_user_room = UserRoom.objects.filter(room=room, user=user)
            if loggedin_user_room.exists():
                loggedin_user_room.first().is_seen = True
                loggedin_user_room.first().save()
            
            # is_seen set to false for other users inside the room
            user_rooms = UserRoom.objects.filter(room=room).exclude(user=user)
            if user_rooms.exists():
                for user_room in user_rooms:
                    user_room.is_seen = False
                    user_room.save()
            return chat_message
        
        except Exception as e:
            logger.error(f'{e} at {str(datetime.datetime.now())} hours!')
    
    @database_sync_to_async
    def check_user_in_conversation(self, conversation):
        try:
            user = User.objects.get(id=self.user.id)
            room = ChatRoom.objects.get(conversation=conversation)
            return self.user in room.users_id.all() 
        except Exception as e:
            logger.error(f'{e} at {str(datetime.datetime.now())} hours!')
    
    
    @database_sync_to_async
    def users_list(self, conversation):
        try:
            room = ChatRoom.objects.get(conversation=conversation)
            return list(room.users_id.all().values_list('id', flat=True))
        except Exception as e:
            logger.error(f'{e} at {str(datetime.datetime.now())} hours!')
    
    
    @database_sync_to_async
    def get_unread_count(self, user_id):
        try:
            rooms = UserRoom.objects.filter(user_id=user_id, is_seen=False)
            return rooms.count()
        except Exception as e:
            logger.error(f'{e} at {str(datetime.datetime.now())} hours!')
        
        