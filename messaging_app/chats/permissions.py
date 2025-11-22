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
