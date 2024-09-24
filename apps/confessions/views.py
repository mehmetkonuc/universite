from django.shortcuts import render, get_object_or_404, redirect
from .models import ConfessionsModel, UserConfessionsFilterModel
from .forms import ConfessionsForm, UserFilterForm
from .filters import UserFilter, MyFilter
from apps.photos.models import PhotosModel
from django.views import View
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Likes
from apps.comments.views import CommentView
from django.contrib import messages
from django.db.models import Count
from django.forms.models import model_to_dict
from django.core.paginator import Paginator


# Create your views here.
class ConfessionsView(View):
    model_data = ConfessionsModel
    user_filter_model = UserConfessionsFilterModel
    filter_form = UserFilter
    user_filter_form = UserFilterForm
    template = 'confessions/index.html'
    context = {'siteTitle': 'İtiraflar'}
    paginate_by = 2

    def get(self, request):
        user_filter, created = self.user_filter_model.objects.get_or_create(user=request.user)
        data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
        # Annotate with like_count and comment_count
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        
        # Apply filters
        filter = self.filter_form(model_to_dict(user_filter), queryset=data)
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
        user_filter = self.user_filter_model.objects.get(user=request.user)
        
        if 'reset_filter' in request.POST:
            # Tüm filtre alanlarını temizle
            for field in model_to_dict(user_filter).keys():
                if field not in ['id', 'user']:  # user ve id hariç tüm alanları temizle
                    setattr(user_filter, field, None)
            user_filter.save()
            return self.get(request)  
        else:
            form = self.user_filter_form(request.POST, instance = user_filter)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.user=request.user
                form_data.save()
            data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
            data = data.annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count('comments', distinct=True)
                )  
            filter = self.filter_form(data=request.POST, queryset=data)
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


class MyConfessionsView(View):
    model_data = ConfessionsModel
    filter_form = MyFilter
    template = 'confessions/my.html'
    context = {'siteTitle': 'İtiraflarım'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=True, user=request.user).order_by('-create_at')
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        
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


class DraftConfessionsView(View):
    model_data = ConfessionsModel
    filter_form = MyFilter
    template = 'confessions/draft.html'
    context = {'siteTitle': 'Taslaklarım'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=False, user=request.user).order_by('-create_at')
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        
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


class ConfessionDetailView(View):
    model_confessions = ConfessionsModel
    model_likes = Likes
    template = 'confessions/details.html'
    paginate_by = 2
    context = {
        }

    def get(self, request, slug):
        confession = get_object_or_404(self.model_confessions, slug=slug)
        liked = confession.likes.filter(user=request.user)
        comments =CommentView.comment_get(content_type=ContentType.objects.get_for_model(confession), object_id=confession.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'siteTitle':confession.title,
            'data': confession,
            'comments': page_obj,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        confession = get_object_or_404(self.model_confessions, slug=slug)
        content_type = ContentType.objects.get_for_model(confession)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=confession.id)
        liked = confession.likes.filter(user=request.user)
        comments =CommentView.comment_get(content_type=ContentType.objects.get_for_model(confession), object_id=confession.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'form': form,
            'data' : confession,
            'comments': page_obj,
            'liked' : liked,
            'liked_comment' : liked_comment,
            })
        return render(request, self.template, self.context)


class ConfessionsAddView(View):
    model_confessions = ConfessionsModel
    model_photos = PhotosModel
    form_confessions = ConfessionsForm
    template = 'confessions/add.html'
    context = {
        'siteTitle': 'İtiraf Ekle',
    }

    def get(self, request):
        
        initial = {'country': request.user.educational_information.country,
                   'university': request.user.educational_information.university,
                   }
        form = self.form_confessions(initial = initial)

        self.context.update({
            'form': form,
        })
        return render(request, self.template, self.context)

    def post(self, request):
        initial = {'country': request.user.educational_information.country,
            'university': request.user.educational_information.university,
            }
        form = self.form_confessions(request.POST, initial=initial)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            if form_data.is_published:
                messages.success(request, 'Başarıyla Kaydedildi ve Yayınlandı')
            else:
                messages.success(request, 'Başarıyla Kaydedildi ve Taslaklara Eklendi.')
            return redirect('confession_details', slug=form_data.slug)


        self.context.update({
            'form': form,
        })

        return render(request, self.template, self.context)


class ConfessionsEditView(View):
    model_confessions = ConfessionsModel
    model_photos = PhotosModel
    form_confessions = ConfessionsForm
    template = 'confessions/add.html'
    context = {
        'siteTitle': 'İtiraf Düzenle',
    }

    def get(self, request, slug):
        instance = self.model_confessions.objects.filter(slug=slug).first()
        form = self.form_confessions(instance = instance)

        self.context.update({
            'form': form,
        })
        return render(request, self.template, self.context)

    def post(self, request, slug):
        instance = self.model_confessions.objects.filter(slug=slug).first()

        form = self.form_confessions(request.POST, instance=instance)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            if form_data.is_published:
                messages.success(request, 'Başarıyla Düzenlendi ve Yayınlandı')
            else:
                messages.success(request, 'Başarıyla Düzenlendi ve Taslaklara Kaydedildi.')
            return redirect('confession_details', slug=form_data.slug)


        self.context.update({
            'form': form,
        })

        return render(request, self.template, self.context)


def delete_confessions(request, confessions_id):
    delete = ConfessionsModel.objects.get(id=confessions_id)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()
        messages.success(request, 'Başarıyla silindi.')
    else:
        messages.success(request, 'Bir hata ile karşılaşıldı.')
        
    return redirect('confessions')