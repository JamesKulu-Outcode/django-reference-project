from rest_framework import status 
from django.conf import settings 
from django.db.models import Max
import uuid
from rest_framework.permissions import (
    IsAuthenticated,
)
from itertools import chain
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView
)
from rest_framework.views import APIView

from .serializers import (
    ChatRoomSerializer,
    ChatRoomDetailSerializer,
    ChatInitSerializer,
    PrivateConversationCreateSerializer,
    ChatReadUpdateSerializer
)
from django.db.models.functions import Concat  
from django.db.models import Value, F, JSONField

from utils.paginators import BasePaginator
from .models import (
    ChatMessage,
    ChatRoom,
    UserRoom 
)


from drf_yasg.utils import swagger_auto_schema
from utils.swagger_schemas import manual_parameters

User = get_user_model()

class ChatRoomDetailView(RetrieveAPIView):
    serializer_class = ChatRoomDetailSerializer
    lookup_field = 'conversation'
    # pagination_class = ChatBasePaginator

    def get_queryset(self):
        return ChatRoom.objects.filter(conversation = self.kwargs['conversation'])


class ChatRoomView(ListAPIView):
    serializer_class = ChatRoomSerializer
    pagination_class = BasePaginator
    
    def get_queryset(self):
        return list(chain(
            ChatRoom.objects.filter(
                users_id=self.request.user,
                is_group=True,
                primary_group=True,
                organization=self.request.user.organization
            ),
            ChatRoom.objects.filter(
                users_id=self.request.user,
                primary_group=False,
                organization=self.request.user.organization
            )
            .annotate(last_message=Max('chatmessage__created_at'))
            .order_by('-last_message'),        
        ))

    @swagger_auto_schema(manual_parameters=manual_parameters)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class ChatReadUpdateView(CreateAPIView):
    serializer_class = ChatReadUpdateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = uuid.UUID(request.data['conversation'])
        chat_room = get_object_or_404(ChatRoom, conversation=conversation)
        user_room = get_object_or_404(UserRoom, room=chat_room, user=request.user)
        user_room.is_seen = True
        user_room.save()
        return Response({"message": "All messages read"}, status=status.HTTP_200_OK)
    

class ChatInitAPI(ListAPIView):
    serializer_class = ChatInitSerializer
    
    def get_queryset(self):
        # add wildcard "keyword"
        return ChatRoom.objects.filter(
            users_id=self.request.user,
            # users_id__organization=self.request.user.organization
        )
        
    def list(self, request):
        response = super().list(request)
        conversations = [data['conversation'] for data in response.data]
        return Response({'conversations':conversations}, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=manual_parameters)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PrivateConversationCreate(CreateAPIView):
    serializer_class = PrivateConversationCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data= {}

        if(request.user == serializer.validated_data['receiver_id']):
            data = {
                "message": "Cannot create conversation with the same user",
                "new_conversation": False
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        user_room = ChatRoom.objects.filter(
            is_group=False,
            users_id=serializer.validated_data['receiver_id']
            ) & ChatRoom.objects.filter(
                is_group=False,
                users_id=request.user.id
            )

        # check if there is conversation already exists else create new conversation
        if user_room.exists():
            data = {
                "message": "Conversation already created for these users.",
                "new_conversation": False,
                "data": ChatRoomSerializer(user_room.first(), context={'request': request}).data,
            }
        else:
            room = ChatRoom.objects.create(
                is_group=False,
                organization=request.user.organization or None
            )
            room.users_id.add(request.user.id)
            room.users_id.add(serializer.validated_data['receiver_id'])
            room.save()

            data = {
                "message": "New conversation created.",
                "new_conversation": True,
                "data": ChatRoomSerializer(room, context={'request': request}).data
            }

        return Response(data, status=status.HTTP_200_OK)