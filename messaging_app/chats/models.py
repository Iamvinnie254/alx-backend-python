import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# --------------------------------------------
# Custom User Model
# --------------------------------------------
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Replaces default 'id' with UUID. Adds phone, role, 
    and created_at timestamp.
    """

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    email = models.EmailField(
        unique=True,
        null=False
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=False
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    # Use email as the unique identifier for auth
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # First name, last name inherited from AbstractUser

    def __str__(self):
        return f"{self.email}"


# --------------------------------------------
# Conversation Model
# --------------------------------------------
class Conversation(models.Model):
    """
    Tracks a conversation between users.
    Supports multiple participants using ManyToManyField.
    """

    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    participants = models.ManyToManyField(
        User,
        related_name="conversations"
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# --------------------------------------------
# Message Model
# --------------------------------------------
class Message(models.Model):
    """
    Stores messages sent by users within a conversation.
    """

    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message_body = models.TextField(
        null=False
    )

    sent_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Message from {self.sender.email}"
