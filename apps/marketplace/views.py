from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from apps.marketplace.models import MarketPlaceModel, MarketPlaceFilterModel, Category, MarketPlaceImagesModel
from apps.marketplace.forms import MarketPlaceForm, FilterForm
from django.contrib.contenttypes.models import ContentType
from apps.marketplace.filters import Filter, MyFilter
from django.db.models import Count
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
class MarketPlaceView(View):
    model_data = MarketPlaceModel
    filter_model = MarketPlaceFilterModel
    filter = Filter
    filter_form = FilterForm
    template = 'marketplace/index.html'
    context = {'siteTitle': 'İlanlar'}
    paginate_by = 4

    def get(self, request):
        user_filter, created = self.filter_model.objects.get_or_create(user=request.user)
        data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
        
        # Apply filters
        filter = self.filter(model_to_dict(user_filter), queryset=data, request=request)
        filtered_data = filter.qs
        
        # Apply sorting
        sorted_data = filtered_data
        
        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter,
            'user_filter': user_filter,
        })
        return render(request, self.template, self.context)

    def post(self, request):
        user_filter = self.filter_model.objects.get(user=request.user)
        
        if 'reset_filter' in request.POST:
            # Tüm filtre alanlarını temizle
            for field in model_to_dict(user_filter).keys():
                if field not in ['id', 'user']:  # user ve id hariç tüm alanları temizle
                    setattr(user_filter, field, None)
            user_filter.save()
            return self.get(request)  
        else:
            form = self.filter_form(request.POST, instance = user_filter)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.user=request.user
                form_data.save()
            data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
 
            filter = self.filter(data=request.POST, queryset=data, request=request)
            filtered_data = filter.qs
            # Apply sorting
            sorted_data = filtered_data
            
            # Pagination
            paginator = Paginator(sorted_data, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            self.context.update({
                'data': page_obj,
                'filter': filter,
                'user_filter': user_filter,
            })
            return render(request, self.template, self.context)


class MyMarketPlaceView(View):
    model_data = MarketPlaceModel
    filter_form = MyFilter
    template = 'marketplace/my.html'
    context = {'siteTitle': 'İlanlarım'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=True, user=request.user).order_by('-create_at')

        # Apply filters
        if 'reset_filter' in request.GET:
            filter = self.filter_form(queryset=data)
        else:
            filter = self.filter_form(request.GET, queryset=data)
            
        filtered_data = filter.qs
        
        # Apply sorting
        sorted_data = filtered_data
        
        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter,
        })
        return render(request, self.template, self.context)


class DraftMarketPlaceView(View):
    model_data = MarketPlaceModel
    filter_form = MyFilter
    template = 'marketplace/draft.html'
    context = {'siteTitle': 'Taslaklarım'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=False, user=request.user).order_by('-create_at')

        # Apply filters
        if 'reset_filter' in request.GET:
            filter = self.filter_form(queryset=data)
        else:
            filter = self.filter_form(request.GET, queryset=data)
            
        filtered_data = filter.qs
        
        # Apply sorting
        sorted_data = filtered_data
        
        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter,
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
        # categories = self.model_category.objects.filter(parent__isnull=True)
        self.context.update({
            'form' : form,
            # 'categories' : categories
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
            if form_data.is_published:
                messages.success(request, 'Başarıyla Yayınlandı')
            else:
                messages.success(request, 'Başarıyla Taslaklara Kaydedildi.')

            return redirect('marketplace_details', slug=form_data.slug)

        # categories = self.model_category.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
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
        # categories = self.model_category.objects.filter(parent__isnull=True)
        return {
            'siteTitle': 'İlan Oluştur',
            'form': form,
            'instance': instance,
            # 'categories': categories,
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
            if form_data.is_published:
                messages.success(request, 'Başarıyla Yayınlandı')
            else:
                messages.success(request, 'Başarıyla Taslaklara Kaydedildi.')

            return redirect('marketplace_details', slug=form_data.slug)

        # If form is not valid, return the form with errors
        context = self.get_context_data(instance=instance, form=form)
        return render(request, self.template, context)


def delete_marketplace(request, marketplace_id):
    delete = MarketPlaceModel.objects.get(id=marketplace_id)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()
        messages.success(request, 'Başarıyla silindi.')

    return redirect('my_marketplace')