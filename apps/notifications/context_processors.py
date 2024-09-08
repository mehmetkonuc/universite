from .models import Notification

def processors(request):
    context = {
            
        }
    if request.user.is_authenticated:
        notifications_header = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        context.update({
                'notifications_header': notifications_header,
            })
    return context