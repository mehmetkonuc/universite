from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.notifications.models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def notification_list(request):
    # Kullanıcının tüm bildirimlerini alıyoruz
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Bildirimlerin okunmadığını işaretleme
    # notifications.update(is_read=True)

    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications/notifications.html', context)


@csrf_exempt
def delete_notifications(request):
    if request.method == "POST":
        data = json.loads(request.body)
        notification_ids = data.get('notification_ids', [])
        Notification.objects.filter(id__in=notification_ids, user=request.user).delete()
        return JsonResponse({"status": "success"})

@csrf_exempt
def mark_notifications_as_read(request):
    if request.method == "POST":
        data = json.loads(request.body)
        notification_ids = data.get('notification_ids', [])
        Notification.objects.filter(id__in=notification_ids, user=request.user).update(is_read=True)
        return JsonResponse({"status": "success"})

@login_required
def notifications_mark_all_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
