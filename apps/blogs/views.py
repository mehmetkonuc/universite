from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.blogs.forms import ArticleAddForm, FilterForm, MyFilterForm
from apps.blogs.models import ArticlesModel, Category, FilterModel
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib import messages
from apps.blogs.filters import ArticleFilter


class ArticlesView(View):
    model_article = ArticlesModel
    filter_form = ArticleFilter
    template = 'blogs/index.html'
    context = {'siteTitle': 'Makaleler'}
    paginate_by = 4

    def get(self, request):
        # Base query set
        articles = self.model_article.objects.filter(is_published=True).order_by('-create_at')
        
        # Annotate with like_count and comment_count
        articles = articles.annotate(
            like_count=Count('likes'),
            comment_count=Count('comments')
        )
        
        # Apply filters
        filter = self.filter_form(request.GET, queryset=articles)
        filtered_articles = filter.qs
        
        # Apply sorting
        sorted_articles = filtered_articles
        
        # Pagination
        paginator = Paginator(sorted_articles, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter
        })
        return render(request, self.template, self.context)


class MyArticlesView(View):
    model_article = ArticlesModel
    filter_form = MyFilterForm
    template = 'blogs/my_articles.html'
    paginate_by = 4
    context = {
        'siteTitle': 'Makaleler',
    }

    def get(self, request):
        articles = self.model_article.objects.filter(is_published=True, user=request.user).order_by('-create_at')
        filter_form = self.filter_form()
        
        paginator = Paginator(articles, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({'data': page_obj, 'filter_form': filter_form})
        return render(request, self.template, self.context)

    def post(self, request):
        if 'reset_filter' in request.POST:
            return self.get(request)
        
        filter_form = self.filter_form(request.POST)

        if filter_form.is_valid():
            articles = self.model_article.objects.filter(is_published=True, user=request.user).order_by('-create_at')
            filter_conditions = Q()
            if filter_form.cleaned_data['category']:
                filter_conditions &= Q(category=filter_form.cleaned_data['category'])
                
            articles = articles.filter(filter_conditions)
            
            if filter_form.cleaned_data['order_by'] == 'likes':
                articles = articles.annotate(like_count=Count('likes')).order_by('-like_count')
            elif filter_form.cleaned_data['order_by'] == 'comments':
                articles = articles.annotate(comment_count=Count('comments')).order_by('-comment_count')      
            
            if filter_form.cleaned_data['search_query']:
                articles = articles.filter(Q(title__icontains=filter_form.cleaned_data['search_query']) | Q(content__icontains=filter_form.cleaned_data['search_query']))
            
        paginator = Paginator(articles, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({'data': page_obj, 'filter_form': filter_form})
        return render(request, self.template, self.context)
  
        
class DraftArticlesView(View):
    model_article = ArticlesModel
    filter_form = MyFilterForm
    template = 'blogs/darft_articles.html'
    paginate_by = 12
    context = {
        'siteTitle': 'Makaleler',
    }

    def get(self, request):
        articles = self.model_article.objects.filter(is_published=False, user=request.user).order_by('-create_at')
        filter_form = self.filter_form()
        
        paginator = Paginator(articles, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({'data': page_obj, 'filter_form': filter_form})
        return render(request, self.template, self.context)

    def post(self, request):
        if 'reset_filter' in request.POST:
            return self.get(request)
        
        filter_form = self.filter_form(request.POST)

        if filter_form.is_valid():
            articles = self.model_article.objects.filter(is_published=False, user=request.user).order_by('-create_at')
            filter_conditions = Q()
            if filter_form.cleaned_data['category']:
                filter_conditions &= Q(category=filter_form.cleaned_data['category'])
                
            articles = articles.filter(filter_conditions)
            
            if filter_form.cleaned_data['order_by'] == 'likes':
                articles = articles.annotate(like_count=Count('likes')).order_by('-like_count')
            elif filter_form.cleaned_data['order_by'] == 'comments':
                articles = articles.annotate(comment_count=Count('comments')).order_by('-comment_count')      
            
            if filter_form.cleaned_data['search_query']:
                articles = articles.filter(Q(title__icontains=filter_form.cleaned_data['search_query']) | Q(content__icontains=filter_form.cleaned_data['search_query']))
            
            
        paginator = Paginator(articles, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({'data': page_obj, 'filter_form': filter_form})
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
    model_likes = Like
    template = 'blogs/details.html'
    context = {
        }

    def get(self, request, slug):
        data = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(data)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'siteTitle':data.title,
            'data': data,
            'comments': comments,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        data = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(data)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=data.id)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'form': form,
            'data' : data,
            'comments': comments,
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
        messages.success(request, 'Makale Başarıyla silindi.')

    return redirect('my_articles')