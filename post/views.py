from django.shortcuts import render, redirect
from django.views import View
from . import forms
from . import models
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
            posts = self.model.objects.filter().order_by('-PublishDate')
            post_images = []
            for post in posts:
                images = models.ImageModel.objects.filter(Post=post)
                post_images.append({
                    'post': post,
                    'images': images
                })

            self.context.update({'form': form,
                                    'posts': posts, 'post_images': post_images})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        if 'AnonymousUser' not in str(request.user):
            form = self.form_class(request.POST)

            if form.is_valid():
                FormSave = form.save(commit=False)
                FormSave.User = request.user
                FormSave.save()
                images = request.FILES.getlist('images')  # 'images' dosya yükleme alanının name attribute'u
                print(images)
                for image in images:
                    models.ImageModel.objects.create(Post=FormSave, Image=image)
            posts = self.model.objects.filter().order_by('-PublishDate')
            self.context.update({'form': form,
                                'posts': posts}) 
        return render(request, self.template_name, self.context)


def DeletePost(request, PostID):
    DeletePost = models.PostsModel.objects.get(id=PostID)
    
    if DeletePost.User == request.user or request.user.is_superuser:
        DeletePost.delete()
        
    return redirect('post')
    