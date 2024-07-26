from django.shortcuts import render, redirect
from django.views import View
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.comments.models import Comment
from apps.comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.photos.models import PhotosModel


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
    like_count = Like.objects.filter(content_type=content_type, object_id=post.id, user=request.user).count()

    return JsonResponse({'liked': liked, 'like_count': like_count})


class PostDetails(View):
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    def get(self, request, post_id):
        post = models.PostsModel.objects.filter(id=post_id).first()
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(models.PostsModel), object_id=post.id).order_by('-created_at')
        post_images = models.ImageModel.objects.filter(Post=post)
        user_liked_posts = models.PostLike.objects.filter(user=request.user).values_list('post_id', flat=True)
        
        form = CommentForm()

        self.context.update({
            'form': form,
            'comments' : comments,
            'post' : post,
            'post_images' :post_images,
            'user_liked_posts':user_liked_posts
        })
        return render(request, "post-detail.html", self.context)
    
    def post(self, request, post_id):
        post = models.PostsModel.objects.filter(id=post_id).first()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = ContentType.objects.get_for_model(models.PostsModel)
            comment.object_id = post.id
            comment.save()
            return redirect('post_detail', post_id=post.id)
        else:
            print('girmedi')
        
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(models.PostsModel), object_id=post.id).order_by('-created_at')
        post_images = models.ImageModel.objects.filter(Post=post)
        user_liked_posts = models.PostLike.objects.filter(user=request.user).values_list('post_id', flat=True)

        self.context.update({
            'form': form,
            'comments' : comments,
            'post' : post,
            'post_images' :post_images,
            'user_liked_posts':user_liked_posts
        })
        return render(request, "post/post-detail.html", self.context)