from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from messaging.models import Message

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
