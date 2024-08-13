from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.blogs.forms import ArticleAddForm
from apps.blogs.models import ArticlesModel, Category
from apps.photos.models import PhotosModel
from django.contrib.contenttypes.models import ContentType
from apps.comments.models import Comment
from apps.likes.models import Like
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.comments.views import CommentView

# Create your views here.
class ArticlesView(View):
    model_article = ArticlesModel
    template = 'blogs/index.html'
    context = {
        'siteTitle': 'Makaleler',
    }

    def get(self, request):
        articles = self.model_article.objects.all()

        self.context.update({
            'articles':articles
        })
        return render(request, self.template, self.context)


class ArticleAddView(View):
    model_categories = Category
    model_photos = PhotosModel
    form_article = ArticleAddForm
    template = 'blogs/article-add.html'
    context = {
        'siteTitle': 'Makale Ekle',
    }

    def get(self, request):
        form = self.form_article()
        categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'categories' : categories
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_article(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            futured_image = request.FILES.get('futured_image')
            self.model_photos.objects.create(
                user=request.user,
                content_type=ContentType.objects.get_for_model(form_data),
                object_id=form_data.pk,
                photo=futured_image
            )
            return redirect('article_details', slug=form_data.slug)

        categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'categories' : categories
        })

        return render(request, self.template, self.context)


class ArticlesDetailsView(View):
    model_article = ArticlesModel
    model_likes = Like
    template = 'blogs/article-details.html'
    context = {
        }

    def get(self, request, slug):
        article = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(article)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'siteTitle':article.title,
            'article': article,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        article = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(article)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=article.id)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'form': form,
            'article' : article,
            'liked' : liked,
            'liked_comment' : liked_comment,
            })
        return render(request, self.template, self.context)


def delete_article(request, article_id):
    delete_article = ArticlesModel.objects.get(id=article_id)

    if delete_article.user == request.user or request.user.is_superuser:
        delete_article.delete()

    return redirect('articles')