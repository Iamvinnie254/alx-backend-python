from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation

from rest_framework.decorators import action



# Conversation ViewSet

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participant IDs.
        Expected payload:
        {
            "participants": ["uuid1", "uuid2"]
        }
        """
        participants_ids = request.data.get("participants", [])

        if not participants_ids:
            return Response(
                {"error": "Participants list cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create conversation
        conversation = Conversation.objects.create()

        # Add participants
        participants = User.objects.filter(user_id__in=participants_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# Message ViewSet

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message in an existing conversation.
        Expected payload:
        {
            "sender": "uuid",
            "conversation": "uuid",
            "message_body": "Hello there!"
        }
        """

        sender_id = request.data.get("sender")
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not (sender_id and conversation_id and message_body):
            return Response(
                {"error": "sender, conversation, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create message
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]



# Message ViewSet

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def perform_create(self, serializer):
        """
        Ensure a user can only send a message in a conversation they belong to.
        """
        conversation = serializer.validated_data["conversation"]

        if self.request.user not in conversation.participants.all():
            raise PermissionError("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)