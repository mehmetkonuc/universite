from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.blogs.forms import ArticleAddForm, UserFilterForm
from apps.blogs.models import ArticlesModel, Category, UserFilterModel
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Likes
from apps.comments.views import CommentView
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib import messages
from apps.blogs.filters import UserFilter, MyFilter
from django.forms.models import model_to_dict


class ArticlesView(View):
    model_data = ArticlesModel
    user_filter_model = UserFilterModel
    filter_form = UserFilter
    user_filter_form = UserFilterForm
    template = 'blogs/index.html'
    context = {'siteTitle': 'Makaleler'}
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
        filter = self.filter_form(model_to_dict(user_filter), queryset=data, request=request)
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
            filter = self.filter_form(data=request.POST, queryset=data, request=request)
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


class MyArticlesView(View):
    model_data = ArticlesModel
    filter_form = MyFilter
    template = 'blogs/my.html'
    context = {'siteTitle': 'Makalelerim'}
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
 
        
class DraftArticlesView(View):
    model_data = ArticlesModel
    filter_form = MyFilter
    template = 'blogs/draft.html'
    context = {'siteTitle': 'Makalelerim'}
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


class ArticleAddView(View):
    model_categories = Category
    form_article = ArticleAddForm
    template = 'blogs/add.html'
    context = {
        'siteTitle': 'Makale Ekle',
    }

    def get(self, request):
        form = self.form_article()
        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_article(request.POST, request.FILES)
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            if form_data.is_published:
                messages.success(request, 'Makale Başarıyla Yayınlandı')
            else:
                messages.success(request, 'Makale Başarıyla Taslaklara Kaydedildi.')
                
            return redirect('article_details', slug=form_data.slug)

        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
        })

        return render(request, self.template, self.context)


class ArticlesDetailsView(View):
    model_article = ArticlesModel
    model_likes = Likes
    template = 'blogs/details.html'
    paginate_by = 12
    context = {
        }

    def get(self, request, slug):
        data = get_object_or_404(self.model_article, slug=slug)
        liked = data.likes.filter(user=request.user)
        comments =CommentView.comment_get(content_type=ContentType.objects.get_for_model(data), object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        # comments = data.comments.filter(parent__isnull=True)
        # liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'siteTitle':data.title,
            'data': data,
            'comments': page_obj,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        data = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(data)
        liked = data.likes.filter(user=request.user)
        comments =CommentView.comment_get(content_type=ContentType.objects.get_for_model(data), object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=data.id)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'form': form,
            'data' : data,
            'comments': page_obj,
            'liked' : liked,
            'liked_comment' : liked_comment,
            })
        return render(request, self.template, self.context)


class ArticleEditView(View):
    model_categories = Category
    model_article = ArticlesModel
    form_article = ArticleAddForm
    template = 'blogs/add.html'
    context = {
        'siteTitle': 'Makale Ekle',
    }

    def get(self, request, slug):
        instance = self.model_article.objects.filter(slug=slug).first()
        form = self.form_article(instance = instance)
        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'instance':instance,
            # 'categories' : categories,
            'futured_image_url': instance.futured_image.url if instance.futured_image else None,
        })
        return render(request, self.template, self.context)

    def post(self, request, slug):
        instance = self.model_article.objects.filter(slug=slug).first()
        form = self.form_article(instance=instance, data=request.POST or None, files=request.FILES or None)
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            if form_data.is_published:
                messages.success(request, 'Makale Başarıyla Düzenlendi ve Yayınlandı')
            else:
                messages.success(request, 'Makale Başarıyla Düzenlendi ve Taslaklara Kaydedildi.')
            return redirect('article_details', slug=form_data.slug)

        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'instance':instance,
            # 'categories' : categories
        })

        return render(request, self.template, self.context)


def delete_article(request, article_id):
    delete_article = ArticlesModel.objects.get(id=article_id)

    if delete_article.user == request.user or request.user.is_superuser:
        delete_article.delete()
        messages.success(request, 'Başarıyla silindi.')

    return redirect('my_articles')