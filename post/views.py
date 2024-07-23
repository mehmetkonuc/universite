from django.shortcuts import render, redirect
from django.views import View
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
class PostView(View):
    form_class = forms.PostsForm
    model = models.PostsModel
    
    template_name = 'home.html'
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    
    def get(self, request):
        if 'AnonymousUser' not in str(request.user):
            form = self.form_class()
            posts = self.model.objects.all().order_by('-PublishDate')
            user_liked_posts = models.PostLike.objects.filter(user=request.user).values_list('post_id', flat=True)

            post_images = []
            for post in posts:
                images = models.ImageModel.objects.filter(Post=post)
                post_images.append({
                    'post': post,
                    'images': images,
                })
            
            self.context.update({
                'form': form,
                'posts': posts,
                'post_images': post_images,
                'user_liked_posts':user_liked_posts

            })
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        if 'AnonymousUser' not in str(request.user):
            form = self.form_class(request.POST)

            if form.is_valid():
                FormSave = form.save(commit=False)
                FormSave.User = request.user
                FormSave.save()
                images = request.FILES.getlist('images')
                for image in images:
                    models.ImageModel.objects.create(Post=FormSave, Image=image)
                

            posts = self.model.objects.all().order_by('-PublishDate')
            user_liked_posts = models.PostLike.objects.filter(user=request.user).values_list('post_id', flat=True)

            post_images = []
            for post in posts:
                images = models.ImageModel.objects.filter(Post=post)
                post_images.append({
                    'post': post,
                    'images': images
                })
            self.context.update({
                'form': form,
                'posts': posts,
                'post_images': post_images,
                'user_liked_posts':user_liked_posts

            })
        return render(request, self.template_name, self.context)


def DeletePost(request, PostID):
    DeletePost = models.PostsModel.objects.get(id=PostID)
    
    if DeletePost.User == request.user or request.user.is_superuser:
        DeletePost.delete()
        
    return redirect('post')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(models.PostsModel, id=post_id)
    user = request.user

    # Kullanıcının bu postu daha önce beğenip beğenmediğini kontrol et
    like, created = models.PostLike.objects.get_or_create(user=user, post=post)

    if not created:
        # Eğer beğeni zaten varsa, beğeniyi kaldır
        like.delete()
        liked = False
    else:
        liked = True

    # Beğeni sayısını güncelle
    like_count = post.postlike_set.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})

class PostDetails(View):
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    def get(self, request, PostID):
        form = forms.PostsComment()
        PostComment = models.PostComment.objects.filter(id=PostID)
        post = models.PostsModel.objects.filter(id=PostID).first()
        post_images = models.ImageModel.objects.filter(Post=post)
        user_liked_posts = models.PostLike.objects.filter(user=request.user).values_list('post_id', flat=True)

        self.context.update({
            'form': form,
            'PostComment' : PostComment,
            'post' : post,
            'post_images' :post_images,
            'user_liked_posts':user_liked_posts
        })
        return render(request, "post/PostDetails.html", self.context)