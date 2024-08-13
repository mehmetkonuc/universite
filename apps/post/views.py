from django.shortcuts import render, redirect
from django.views import View
from . import forms
from . import models
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.photos.models import PhotosModel
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
            liked = self.model_like.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
                    
            self.context.update({
                'form': form,
                'posts': posts,
                'liked':liked
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
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=post.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        form = CommentView.form_class()

        self.context.update({
            'form': form,
            'post' : post,
            'comments' : comments,
            'liked':liked,
            'liked_comment': liked_comment,
        })
        return render(request, self.template, self.context)
    
    def post(self, request, post_id):
        post = self.model_posts.objects.filter(id=post_id).first()
        content_type = ContentType.objects.get_for_model(post)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=post_id)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=post.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        
        self.context.update({
            'form': form,
            'post' : post,
            'comments' : comments,
            'liked':liked,
            'liked_comment': liked_comment,
            })
        return render(request, self.template, self.context)