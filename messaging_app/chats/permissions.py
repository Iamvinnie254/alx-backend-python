from rest_framework.permissions import BasePermission

class IsOwnerOfConversation(BasePermission):
    """
    Only allow users to access conversations that belong to them.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsOwnerOfMessage(BasePermission):
    """
    Ensure users only access their own messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user

from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of a conversation.
    Ensures users can only send, view, update, or delete messages
    in conversations where they are participants.
    """

    def has_object_permission(self, request, view, obj):
        """
        obj will be either a Conversation or a Message instance.
        We check if the authenticated user is part of that conversation.
        """

        # If obj is a conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If obj is a message, check conversation participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
