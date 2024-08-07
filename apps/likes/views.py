from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from apps.likes.models import Like

# Create your views here.
@require_POST
def like_object(request):
    content_type_id = request.POST.get('content_type_id')
    object_id = request.POST.get('object_id')
    content_type = get_object_or_404(ContentType, id=content_type_id)
    model_class = content_type.model_class()
    obj = get_object_or_404(model_class, id=object_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=obj.id
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = Like.objects.filter(content_type=content_type, object_id=obj.id).count()

    return JsonResponse({'liked': liked, 'like_count': like_count})