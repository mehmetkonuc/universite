from .models import Notification
from apps.chat.models import Chat, Message
from django.db.models import Q, Max
from apps.follow.models import Follow, FollowRequest
from django.core.paginator import Paginator



def processors(request):
    context = {
            
        }
    if request.user.is_authenticated:
        notifications_header = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        notifications_count = notifications_header.count()

        chats = Chat.objects.filter(
                Q(first_user=request.user) | Q(second_user=request.user)
            ).annotate(
                last_message_time=Max('message__timestamp')
            ).order_by('-last_message_time')
        
        for chat in chats:
            messages = Message.objects.filter(chat=chat, receiver=request.user, is_read=False)
            if not messages:
                chats = chats.exclude(id=chat.id)

        chat_count = chats.count()

        # followers = Follow.objects.filter(following=request.user, is_read=False)
        if request.user.privacy.is_private:
            followers = request.user.follow_requests_received.filter(is_read=False, is_approved = False)
        else:
            followers = request.user.follow_requests_received.filter(is_read=False)

        context.update({
                'notifications_header': notifications_header[:6],
                'notifications_count':notifications_count,
                'chats_header' : chats[:6],
                'chat_count' : chat_count,
                'followers_header' : followers,
            })
    return context