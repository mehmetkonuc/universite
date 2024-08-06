from django.shortcuts import render, redirect
from django.views import View
from apps.blogs.forms import ArticleAddForm
from apps.blogs.models import ArticlesModel
from apps.photos.models import PhotosModel
from django.contrib.contenttypes.models import ContentType
from apps.comments.forms import CommentForm
from apps.comments.models import Comment

# Create your views here.
class ArticleAddView(View):
    def get(self, request):
        form = ArticleAddForm()
        context = {
            'form': form,
        }
        return render(request, 'blogs/article-add.html', context)

    def post(self, request):
        form = ArticleAddForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            futured_image = request.FILES.get('futured_image')
            PhotosModel.objects.create(
                user=request.user,
                content_type=ContentType.objects.get_for_model(form_data),
                object_id=form_data.pk,
                photo=futured_image
            )
        context = {
            'form': form,
        }
        
        return render(request, 'blogs/article-add.html', context)

class ArticlesView(View):
    def get(self, request):
        articles = ArticlesModel.objects.all()

        context = {
            'articles':articles
        }
        return render(request, 'blogs/index.html', context)

class ArticlesDetailsView(View):
    form_class = CommentForm
    model_comments = Comment

    def get(self, request, article_id):
        article = ArticlesModel.objects.filter(pk=article_id).first()
        content_type = ContentType.objects.get_for_model(article)
        comments = self.model_comments.objects.filter(content_type=content_type, object_id=article.id).order_by('-created_at')

        context = {
            'article':article,
            'comments' :comments
        }
        return render(request, 'blogs/article-details.html', context)

    def post(self, request, article_id):
        article = ArticlesModel.objects.filter(pk=article_id).first()

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
            return redirect('article_details', article_id=article.id)
        
        comments = self.model_comments.objects.filter(content_type=content_type, object_id=article.id).order_by('-created_at')
        # user_liked_posts = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        
        context = {
            'form': form,
            'comments' : comments,
            'article' : article,
            # 'user_liked_posts':user_liked_posts
        }
        return render(request, "blogs/article-details.html", context)