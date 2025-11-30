from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    # Logout the user first
    logout(request)
    # Delete the user account
    user.delete()
    return redirect('home')  # Redirect to home or goodbye page

def get_all_replies(message):
    replies = []
    for reply in message.replies.all():  # uses the related_name, not a filter on Message
        replies.append({
            'reply': reply,
            'replies': get_all_replies(reply)  # recursion
        })
    return replies


def threaded_conversation(request, message_id):
    main_message = Message.objects.select_related('sender', 'receiver').get(pk=message_id)
    nested_replies = get_all_replies(main_message)

    # Prefetch all replies (and their sender/receiver) efficiently
    replies = get_all_replies(main_message)  # nested structure

    context = {
        'message': main_message,
        'replies': nested_replies
    }
    return render(request, 'messaging/threaded_conversation.html', context)