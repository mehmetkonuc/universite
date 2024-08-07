from django.shortcuts import render, redirect
from django.views import View
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.photos.models import PhotosModel
from django.urls import reverse
from apps.comments.views import CommentView

# Create your views here.
class PostView(View):
    form_class = forms.PostsForm
    model_post = models.PostsModel
    model_like = Like
    model_photos = PhotosModel
    template_name = 'home.html'
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    
    def get(self, request):
        if 'AnonymousUser' not in str(request.user):
            form = self.form_class()
            posts = self.model_post.objects.all().order_by('-PublishDate')
            content_type = ContentType.objects.get_for_model(self.model_post)
            user_liked_posts = self.model_like.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
                    
            self.context.update({
                'form': form,
                'posts': posts,
                'user_liked_posts':user_liked_posts
            })
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        if 'AnonymousUser' not in str(request.user):
            form = self.form_class(request.POST)

            if form.is_valid():
                form_save = form.save(commit=False)
                form_save.User = request.user
                form_save.save()
                images = request.FILES.getlist('images')
                for image in images:
                    self.model_photos.objects.create(
                        user=request.user,
                        content_type=ContentType.objects.get_for_model(form_save),
                        object_id=form_save.pk,
                        photo=image
                    )
          
            posts = self.model_post.objects.all().order_by('-PublishDate')
            content_type = ContentType.objects.get_for_model(self.model_post)
            user_liked_posts = self.model_like.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)

            self.context.update({
                'form': form,
                'posts': posts,
                'user_liked_posts':user_liked_posts

            })
        return render(request, self.template_name, self.context)


def delete_post(request, PostID):
    delete_post = models.PostsModel.objects.get(id=PostID)
    
    if delete_post.User == request.user or request.user.is_superuser:
        delete_post.delete()
        
    return redirect('post')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(models.PostsModel, id=post_id)
    content_type = ContentType.objects.get_for_model(post)

    # Kullanıcının bu postu daha önce beğenip beğenmediğini kontrol et
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=post.id
    )

    if not created:
        # Eğer beğeni zaten varsa, beğeniyi kaldır
        like.delete()
        liked = False
    else:
        liked = True

    # Beğeni sayısını güncelle
    like_count = Like.objects.filter(content_type=content_type, object_id=post.id).count()

    return JsonResponse({'liked': liked, 'like_count': like_count})


class PostDetails(View):
    model_posts = models.PostsModel
    model_likes = Like
    template = 'post-detail.html'
    context = {
        'siteTitle': 'Yorumlar',
    }
    def get(self, request, post_id):
        post = self.model_posts.objects.filter(id=post_id).first()
        content_type = ContentType.objects.get_for_model(self.model_posts)
        user_liked_posts = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        user_liked_comments = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        form = CommentView.form_class()

        self.context.update({
            'form': form,
            'post' : post,
            'user_liked_posts':user_liked_posts,
            'user_liked_comments': user_liked_comments,
        })
        return render(request, self.template, self.context)
    
    def post(self, request, post_id):
        post = self.model_posts.objects.filter(id=post_id).first()
        content_type = ContentType.objects.get_for_model(post)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=post_id)
        user_liked_posts = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        user_liked_comments = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        
        self.context.update({
            'form': form,
            'post' : post,
            'user_liked_posts':user_liked_posts,
            'user_liked_comments': user_liked_comments,
            })
        return render(request, self.template, self.context)


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