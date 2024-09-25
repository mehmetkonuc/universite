from .models import Notification
from apps.chat.models import Chat, Message
from django.db.models import Q, Max
from apps.follow.models import Follow, FollowRequest
def processors(request):
    context = {
            
        }
    if request.user.is_authenticated:
        notifications_header = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')

        chats = Chat.objects.filter(
                Q(first_user=request.user) | Q(second_user=request.user)
            ).annotate(
                last_message_time=Max('message__timestamp')
            ).order_by('-last_message_time')
        
        for chat in chats:
            messages = Message.objects.filter(chat=chat, receiver=request.user, is_read=False)
            if not messages:
                chats = chats.exclude(id=chat.id)

        # followers = Follow.objects.filter(following=request.user, is_read=False)
        followers = request.user.follow_requests_received.filter(is_read=False)
        context.update({
                'notifications_header': notifications_header,
                'chats_header' : chats,
                'followers_header' : followers,
            })
    return context