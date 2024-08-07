from django.contrib.contenttypes.models import ContentType
from apps.photos.models import PhotosModel

# Create your views here.
def photos_save(request, model):
    model_photos = PhotosModel
    images = request.FILES.getlist('images')
    for image in images:
        model_photos.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(model),
            object_id=model.id,
            photo=image
        )