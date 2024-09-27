from django.shortcuts import get_object_or_404, redirect, render
from .models import Follow, FollowRequest
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


@login_required
def toggle_follow(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_to_follow = get_object_or_404(User, id=user_id)

        if request.user == user_to_follow:
            return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself'}, status=400)

        # Gizlilik durumu kontrol ediliyor
        if user_to_follow.privacy.is_private:
            follow, follow_request, status = _handle_private_account_follow(request.user, user_to_follow)
        else:
            follow, follow_request, status = _handle_public_account_follow(request.user, user_to_follow)

        # Takip durumu sonuçlarını dönüyoruz
        return JsonResponse({'status': status})

    return JsonResponse({'status': 'error'}, status=400)


def _handle_private_account_follow(follower, user_to_follow):
    """Gizli hesaplar için takip isteklerini yöneten yardımcı fonksiyon."""
    try:
        follow = Follow.objects.get(follower=follower, following=user_to_follow)
        follow.delete()
        FollowRequest.objects.filter(follower=follower, following=user_to_follow).delete()
        return None, None, 'unfollowed'  # Unfollow işlemi
    except Follow.DoesNotExist:
        follow_request, created = FollowRequest.objects.get_or_create(follower=follower, following=user_to_follow)
        if created:
            return None, follow_request, 'request_sent'  # Takip isteği gönderildi
        else:
            follow_request.delete()
            return None, None, 'cancel_request'  # Takip isteği iptal edildi


def _handle_public_account_follow(follower, user_to_follow):
    """Gizli olmayan hesaplar için takip işlemlerini yöneten yardımcı fonksiyon."""
    follow, created = Follow.objects.get_or_create(follower=follower, following=user_to_follow)
    
    if created:
        FollowRequest.objects.create(follower=follower, following=user_to_follow, is_approved=True)  # Var olan takip isteği varsa sil
        return follow, None, 'followed'  # Direkt takip edildi
    else:
        FollowRequest.objects.filter(follower=follower, following=user_to_follow).delete()  # Var olan takip isteği varsa sil
        follow.delete()
        return None, None, 'unfollowed'  # Unfollow işlemi


@login_required
def follow_requests_view(request):
    follow_requests = FollowRequest.objects.filter(following=request.user).order_by('-created_at')
    follow_requests.filter(is_read=False).update(is_read=True)

    paginator = Paginator(follow_requests, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'follow/follow_requests.html', {'follow_requests': page_obj})


@login_required
def follow_requests_action(request):
    if request.method == "POST":
        follow_request_id = request.POST.get('follow_request_id')
        action = request.POST.get('action')  # 'approve' ya da 'reject' olacak
        
        follow_request = get_object_or_404(FollowRequest, id=follow_request_id)

        if follow_request.following == request.user:
            if action == "approve":
                # Takip isteği onaylandı
                Follow.objects.create(follower=follow_request.follower, following=follow_request.following)
                follow_request.is_approved = True
                follow_request.save()  # Takip isteğini sildik

                # Takip isteğini onayla
                follow_request.status = 'approved'

                return JsonResponse({'status': 'approved'})
            
            elif action == "reject":
                # Takip isteğini reddet
                follow_request.status = 'rejected'
                follow_request.delete()
                return JsonResponse({'status': 'rejected'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
@csrf_exempt
def follow_requests_delete(request):
    if request.method == 'POST':
        selected_followers = request.POST.getlist('selected_followers[]')  # 'selected_followers[]' listesini al
        if selected_followers:
            # Kullanıcıya ait verileri sil
            deleted, _ = FollowRequest.objects.filter(id__in=selected_followers, following=request.user).delete()
            
            # Silme işleminin sonucuna göre response dön
            if deleted:
                return JsonResponse({'status': 'success', 'message': 'Seçili takip istekleri silindi.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Takip istekleri silinemedi.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Seçili takip isteği yok.'})
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'})


@login_required
def followers_mark_all_as_read(request):
    if request.method == 'POST':
        FollowRequest.objects.filter(following=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)