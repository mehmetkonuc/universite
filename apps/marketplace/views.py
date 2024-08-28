from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from apps.marketplace.models import MarketPlaceModel, Category, MarketPlaceImagesModel
from apps.marketplace.forms import MarketPlaceForm
from django.contrib.contenttypes.models import ContentType
from apps.photos.models import PhotosModel

# Create your views here.
class MarketPlaceView(View):
    model_marketplace = MarketPlaceModel
    template = 'marketplace/index.html'
    context = {
        'siteTitle': 'İlanlar',
    }

    def get(self, request):
        marketplaces = self.model_marketplace.objects.all()

        self.context.update({
            'data':marketplaces
        })
        return render(request, self.template, self.context)


class MarketPlaceAddView(View):
    model_marketplace = MarketPlaceModel
    model_images = MarketPlaceImagesModel
    form_marketplace = MarketPlaceForm
    template = 'marketplace/add.html'
    context = {
        'siteTitle' : 'İlan Ekle'
    }
    def get(self, request):
        form = self.form_marketplace()
        categories = Category.objects.filter(parent__isnull=True)
        self.context.update({
            'form' : form,
            'categories' : categories
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_marketplace(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            images = request.FILES.getlist('images')
            for image in images:
                self.model_images.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(form_data),
                    object_id=form_data.pk,
                    image=image
                )
            return redirect('article_details', slug=form_data.slug)

        categories = Category.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'categories' : categories
        })

        return render(request, self.template, self.context)


class MarketPlaceDetailsView(View):
    model_marketplace = MarketPlaceModel
    template = 'marketplace/details.html'
    context = {
        }

    def get(self, request, slug):
        data = get_object_or_404(self.model_marketplace, slug=slug)

        self.context.update({
            'siteTitle':data.title,
            'data': data,
        })

        return render(request, self.template, self.context)
