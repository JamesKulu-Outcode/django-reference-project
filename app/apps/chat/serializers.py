from rest_framework import serializers
from .models import ChatMessage, ChatRoom, UserRoom
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
import json
from django.db.models import F
from django.db.models.functions import Concat  
from django.db.models import Value as V 
from django.utils import timezone
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from utils.paginator_meta import get_meta
from utils.paginators import BasePaginator


User = get_user_model()

# class ChatMessageSerializer(serializers.ModelSerializer):
#    class Meta:
#       model = ChatMessage
#       fields = (
#          # 'room_id',
#          'message',
#          'user_id',
#          'is_read',
#          'created_at'
#          )
   
#    def to_representation(self, instance):
#       data = super(ChatMessageSerializer, self).to_representation(instance)
#       messages = ChatMessage.objects.filter(room_id=instance.room_id).values('id', 'message', 'created_at', sender=F('user_id'))
#       # ids = [message['sender'] for message in messages]
#       # user_ids = User.objects.filter(id__in=ids).values('id', full_name=Concat('first_name', V(' '), 'last_name'))
      
#       # del data['room_id']
#       del data['message']
#       # del data['is_read']
#       # del data['user_id']
#       # del data['created_at']
#       data.update({'conversation': f'{self.context.get("request").user.first_name} {self.context.get("request").user.last_name}'})
#       # data.update({'full_name': f'{instance.user_id.first_name} {instance.user_id.last_name}'})
#       # data.update({'start_date': timezone.now()})
#       # data.update({'room_name': instance.room_id.conversation})
#       # data.update({'user_ids': user_ids})
#       data.update({'messages': messages})

#       return data
        

class ChatRoomSerializer(serializers.ModelSerializer):
   class Meta:
      model = ChatRoom
      fields = (
         'id',
         'conversation',
         'name',
         'is_group',
         'primary_group',
         'created_at'
         )

   def to_representation(self, instance):
      data = super(ChatRoomSerializer, self).to_representation(instance)
      messages = ChatMessage.objects.filter(room_id=instance.id)
      messages_count = messages.count()
      
      chat_to = instance.users_id.filter(~Q(id = self.context.get("request").user.id)) # getting all users in room except loggedin user
      
      if chat_to.exists() and instance.is_group == False:
         data.update({'first_name': chat_to[0].first_name})
         data.update({'last_name': chat_to[0].last_name})
      else:
         data.update({'first_name': None})
         data.update({'last_name': None})
         
      # data.update({'is_seen': False if messages_count > 0 else True}) 
      
      # is_seen is set to true for their own message
      # if ChatRoom.objects.filter(chatmessage__user_id=self.context.get("request").user).exists():
      #    data.update({'is_seen': True})
      # else:
      #    user_room = UserRoom.objects.filter(room=instance, user=self.context.get("request").user)
      #    data.update({
      #       'is_seen': user_room.first().is_seen if user_room.exists() else False
      #    })
      
      data.update({'is_seen': UserRoom.objects.filter(user=self.context.get("request").user, room=instance).first().is_seen}) 
      data.update({'image': ''}) 
      data.update({'new_message_count': messages_count}) 
      data.update({'conversation_id': instance.id}) 
      data.update({"last_message": messages.last().message if messages.exists() else ''})

      return data


class UserMessageSerializer(serializers.ModelSerializer):
   full_name = serializers.SerializerMethodField()
   
   def get_full_name(self, obj):
      return f'{obj.first_name} {obj.last_name}'
   
   class Meta:
      model = User
      fields = ('id', 'full_name')


class ChatMessageSerializer(serializers.ModelSerializer):
   sender = UserMessageSerializer(source='user_id')
   
   class Meta:
      model = ChatMessage
      fields = ('id', 'message', 'created_at', 'sender')


class ChatRoomDetailSerializer(serializers.ModelSerializer):
   class Meta:
      model = ChatRoom
      fields = ('id',)
   
   def to_representation(self, instance):
      data = super(ChatRoomDetailSerializer, self).to_representation(instance)
      
      chat_room = get_object_or_404(ChatRoom, conversation=instance.conversation)
      user_room = get_object_or_404(UserRoom, room=chat_room, user=self.context.get("request").user)
      user_room.is_seen = True
      user_room.save()
      
      messages = ChatMessage.objects.filter(room_id=instance.id).order_by('-created_at')
      
      # ids = [message['sender'] for message in messages]
      # user_ids = User.objects.filter(id__in=ids).values('id', full_name=Concat('first_name', V(' '), 'last_name'))
      data.update({'conversation': f'{self.context.get("request").user.first_name} {self.context.get("request").user.last_name}'})
      data.update({'start_date': instance.created_at})
      data.update({'room_name': instance.conversation})
      
      paginator = BasePaginator()
      result_page = paginator.paginate_queryset(messages, self.context.get("request"))
      serializer = ChatMessageSerializer(result_page, many=True)
      data.update({"messages": serializer.data})

      return get_meta(paginator, data)


class ChatInitSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = ChatRoom
      fields = ('conversation',)
   
   
class PrivateConversationCreateSerializer(serializers.Serializer):
   receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class ChatReadUpdateSerializer(serializers.Serializer):
   conversation = serializers.SlugRelatedField(
        slug_field='conversation',
        queryset=ChatRoom.objects.all() # Might be redundant with read_only=True
    )