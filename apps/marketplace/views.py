from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from apps.marketplace.models import MarketPlaceModel, Category, MarketPlaceImagesModel
from apps.marketplace.forms import MarketPlaceForm
from django.contrib.contenttypes.models import ContentType

# Create your views here.
class MarketPlaceView(View):
    model_marketplace = MarketPlaceModel
    template = 'marketplace/index.html'
    context = {
        'siteTitle': 'İlanlar',
    }

    def get(self, request):
        marketplaces = self.model_marketplace.objects.filter(is_published=True)

        self.context.update({
            'data':marketplaces
        })
        return render(request, self.template, self.context)


class MyMarketPlaceView(View):
    model_marketplace = MarketPlaceModel
    template = 'marketplace/my_marketplace.html'
    context = {
        'siteTitle': 'İlanlar',
    }

    def get(self, request):
        marketplaces = self.model_marketplace.objects.filter(user=request.user, is_published=True)

        self.context.update({
            'data':marketplaces
        })
        return render(request, self.template, self.context)


class MyDraftMarketPlaceView(View):
    model_marketplace = MarketPlaceModel
    template = 'marketplace/my_draft_marketplace.html'
    context = {
        'siteTitle': 'İlanlar',
    }

    def get(self, request):
        marketplaces = self.model_marketplace.objects.filter(user=request.user, is_published=False)

        self.context.update({
            'data':marketplaces
        })
        return render(request, self.template, self.context)


class MarketPlaceAddView(View):
    model_marketplace = MarketPlaceModel
    model_images = MarketPlaceImagesModel
    form_marketplace = MarketPlaceForm
    model_category = Category
    template = 'marketplace/add.html'
    context = {
        'siteTitle' : 'İlan Ekle'
    }
    def get(self, request):
        form = self.form_marketplace()
        categories = self.model_category.objects.filter(parent__isnull=True)
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
            return redirect('marketplace_details', slug=form_data.slug)

        categories = self.model_category.objects.filter(parent__isnull=True)

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


class MarketPlaceEditView(View):
    model_marketplace = MarketPlaceModel
    model_images = MarketPlaceImagesModel
    model_category = Category
    form_marketplace = MarketPlaceForm
    template = 'marketplace/add.html'

    def get_context_data(self, instance=None, form=None):
        categories = self.model_category.objects.filter(parent__isnull=True)
        return {
            'siteTitle': 'İlan Oluştur',
            'form': form,
            'instance': instance,
            'categories': categories,
        }

    def get(self, request, slug):
        instance = get_object_or_404(self.model_marketplace, slug=slug)
        form = self.form_marketplace(instance=instance)
        context = self.get_context_data(instance=instance, form=form)
        return render(request, self.template, context)

    def post(self, request, slug):
        instance = get_object_or_404(self.model_marketplace, slug=slug)
        form = self.form_marketplace(instance=instance, data=request.POST, files=request.FILES)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()

            # Handle image uploads
            images = request.FILES.getlist('images')
            for image in images:
                self.model_images.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(form_data),
                    object_id=form_data.pk,
                    image=image
                )

            # Handle deleted images
            deleted_images = request.POST.get('deleted_images')
            if deleted_images:
                image_ids = deleted_images.split(',')
                self.model_images.objects.filter(id__in=image_ids).delete()

            return redirect('marketplace_details', slug=form_data.slug)

        # If form is not valid, return the form with errors
        context = self.get_context_data(instance=instance, form=form)
        return render(request, self.template, context)


def delete_marketplace(request, marketplace_id):
    delete = MarketPlaceModel.objects.get(id=marketplace_id)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()

    return redirect('marketplace')