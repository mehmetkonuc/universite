from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.blogs.forms import ArticleAddForm
from apps.blogs.models import ArticlesModel, Category
from apps.photos.models import PhotosModel
from django.contrib.contenttypes.models import ContentType
from apps.comments.forms import CommentForm
from apps.comments.models import Comment
from apps.likes.models import Like
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
    model_comments = Comment
    model_photos = PhotosModel
    model_likes = Like
    form_class = CommentForm
    template = 'blogs/article-details.html'
    context = {
        }

    def get(self, request, slug):
        article = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(article)
        comments = self.model_comments.objects.filter(content_type=content_type, object_id=article.id).order_by('-created_at')
        user_liked_article = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        user_liked_comments = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(self.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'siteTitle':article.title,
            'article': article,
            'comments': comments,
            'user_liked_article' : user_liked_article,
            'user_liked_comments' : user_liked_comments,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        article = get_object_or_404(self.model_article, slug=slug)
        content_type = ContentType.objects.get_for_model(article)
        form = self.form_class(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = article.id
            comment.save()
            
            images = request.FILES.getlist('images')
            for image in images:
                self.model_photos.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(comment),
                    object_id=comment.pk,
                    photo=image
                )
            return redirect('article_details', slug=article.slug)
        
        comments = self.model_comments.objects.filter(content_type=content_type, object_id=article.id).order_by('-created_at')
        user_liked_article = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        
        self.context.update({
            'form': form,
            'comments' : comments,
            'article' : article,
            'user_liked_article' : user_liked_article

            })
        return render(request, self.template, self.context)


def delete_article(request, article_id):
    delete_article = ArticlesModel.objects.get(id=article_id)
    
    if delete_article.user == request.user or request.user.is_superuser:
        delete_article.delete()
        
    return redirect('articles')


def delete_comment(request, comment_id):
    delete_comment = Comment.objects.get(id=comment_id)
    
    if delete_comment.user == request.user or request.user.is_superuser:
        delete_comment.delete()
    
    article = ArticlesModel.objects.get(id=delete_comment.object_id)

    return redirect('article_details', slug=article.slug)


@login_required
def like_article(request, article_id):
    article = get_object_or_404(ArticlesModel, id=article_id)
    content_type = ContentType.objects.get_for_model(article)

    # Kullanıcının bu postu daha önce beğenip beğenmediğini kontrol et
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=article.id
    )

    if not created:
        # Eğer beğeni zaten varsa, beğeniyi kaldır
        like.delete()
        liked = False
    else:
        liked = True

    # Beğeni sayısını güncelle
    like_count = Like.objects.filter(content_type=content_type, object_id=article.id).count()

    return JsonResponse({'liked': liked, 'like_count': like_count})


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    content_type = ContentType.objects.get_for_model(comment)

    # Kullanıcının bu postu daha önce beğenip beğenmediğini kontrol et
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=comment.id
    )

    if not created:
        # Eğer beğeni zaten varsa, beğeniyi kaldır
        like.delete()
        liked = False
    else:
        liked = True

    # Beğeni sayısını güncelle
    like_count = Like.objects.filter(content_type=content_type, object_id=comment.id).count()

    return JsonResponse({'liked': liked, 'like_count': like_count})