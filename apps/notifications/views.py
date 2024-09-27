from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.notifications.models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator


@login_required
def notification_list(request):
    # Kullanıcının tüm bildirimlerini alıyoruz
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Bildirimlerin okunmadığını işaretleme
    notifications.update(is_read=True)

    paginator = Paginator(notifications, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'notifications': page_obj,
    }
    return render(request, 'notifications/notifications.html', context)


@login_required
def notifications_mark_all_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


@login_required
@csrf_exempt
def notifications_requests_delete(request):
    if request.method == 'POST':
        selected_notifications = request.POST.getlist('selected_notifications[]')  # 'selected_notifications[]' listesini al
        print(selected_notifications)
        if selected_notifications:
            # Kullanıcıya ait verileri sil
            deleted, _ = Notification.objects.filter(id__in=selected_notifications).delete()
            
            # Silme işleminin sonucuna göre response dön
            if deleted:
                return JsonResponse({'status': 'success', 'message': 'Seçili bildirimler silindi.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Bildirimler silinemedi.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Bildirim yok.'})
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'})