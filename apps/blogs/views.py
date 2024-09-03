from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.blogs.forms import ArticleAddForm, UserFilterForm
from apps.blogs.models import ArticlesModel, Category, UserFilterModel
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.db.models import Q, Count

# Create your views here.
class ArticlesView(View):
    model_article = ArticlesModel
    filter_model = UserFilterModel
    filter_form = UserFilterForm
    template = 'blogs/index.html'
    context = {'siteTitle': 'Makaleler'}

    def get(self, request):
        filter_instance = self.filter_model.objects.filter(user=request.user).first()
        articles = self.model_article.objects.filter(is_published=True).order_by('-create_at')

        filter_conditions = Q()
        
        if filter_instance:
            if filter_instance.category:
                filter_conditions &= Q(category=filter_instance.category)

            if filter_instance.university:
                filter_conditions &= Q(user__educationalinformationmodel__University=filter_instance.university)

            if filter_instance.department:
                filter_conditions &= Q(user__educationalinformationmodel__Department=filter_instance.department)

            if filter_instance.status:
                filter_conditions &= Q(user__educationalinformationmodel__Status=filter_instance.status)

            if filter_instance.country:
                filter_conditions &= Q(user__educationalinformationmodel__Country=filter_instance.country)

            articles = articles.filter(filter_conditions)

            if filter_instance.order_by == 'likes':
                articles = articles.annotate(like_count=Count('likes')).order_by('-like_count')
            elif filter_instance.order_by == 'comments':
                articles = articles.annotate(comment_count=Count('comments')).order_by('-comment_count')

        search_query = request.POST.get('search_query')
        if search_query:
            articles = articles.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        filter_form = self.filter_form(instance=filter_instance)
        self.context.update({'data': articles, 'filter_form': filter_form})
        return render(request, self.template, self.context)

    def post(self, request):
        filter = self.filter_model.objects.filter(user=request.user).first()

        if 'reset_filter' in request.POST:
            if filter:
                filter.category = None
                filter.university = None
                filter.department = None
                filter.status = None
                filter.country = None
                filter.order_by = None
                filter.save()
        else:
            filter_form = self.filter_form(request.POST, instance=filter)
            if filter_form.is_valid():
                filter_form_data = filter_form.save(commit=False)
                filter_form_data.user = request.user
                filter_form_data.save()

        return self.get(request)


class MyArticlesView(View):
    model_article = ArticlesModel
    template = 'blogs/my_articles.html'
    context = {
        'siteTitle': 'Makaleler',
    }

    def get(self, request):
        articles = self.model_article.objects.filter(is_published=True, user=request.user)

        self.context.update({
            'data':articles
        })
        return render(request, self.template, self.context)


class MyDraftArticlesView(View):
    model_article = ArticlesModel
    template = 'blogs/my_darft_articles.html'
    context = {
        'siteTitle': 'Makaleler',
    }

    def get(self, request):
        articles = self.model_article.objects.filter(is_published=False, user=request.user)

        self.context.update({
            'data':articles
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

    return redirect('articles')