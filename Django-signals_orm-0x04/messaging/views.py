from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Message
from django.views.decorators.cache import cache_page


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

def inbox(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user)  # Correct usage

    context = {
        'unread_messages': unread_messages
    }
    return render(request, 'messaging/inbox.html', context)


@cache_page(60)  # Cache this view for 60 seconds
def conversation_view(request, message_id):
    main_message = Message.objects.select_related('sender', 'receiver').get(pk=message_id)
    
    # Prefetch replies for performance
    replies = main_message.replies.select_related('sender', 'receiver').all()
    
    context = {
        'message': main_message,
        'replies': replies,
    }
    return render(request, 'messaging/conversation.html', context)

def get_all_replies(message):
    result = []
    for reply in message.replies.select_related('sender', 'receiver').all():
        result.append({
            'reply': reply,
            'replies': get_all_replies(reply)
        })
    return result

@cache_page(60)
def threaded_conversation(request, message_id):
    main_message = Message.objects.select_related('sender', 'receiver').get(pk=message_id)
    nested_replies = get_all_replies(main_message)
    
    return render(request, 'messaging/threaded_conversation.html', {
        'message': main_message,
        'replies': nested_replies
    })
