from django.shortcuts import get_object_or_404, redirect
from .models import Follow
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', user_id=user_id)

def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', user_id=user_id)

@login_required
def toggle_follow(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if request.user != user_to_follow:
            follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
            
            if not created:
                # Zaten takip ediyorsa takipten çıkar
                follow.delete()
                return JsonResponse({'status': 'unfollowed'})
            else:
                return JsonResponse({'status': 'followed'})

    return JsonResponse({'status': 'error'}, status=400)