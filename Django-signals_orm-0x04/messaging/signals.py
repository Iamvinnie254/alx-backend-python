from django.db.models.signals import post_save, pre_save,   post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Automatically create a notification for the receiver
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, no edit to log
        return
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Message content is changing, log the old content
        MessageHistory.objects.create(message=old_message, old_content=old_message.content)
        instance.edited = True

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()