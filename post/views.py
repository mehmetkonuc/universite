from django.shortcuts import render, redirect
from django.views import View
from . import forms
from . import models
# Create your views here.
class PostView(View):
    form_class = forms.PostsForm
    model = models.PostsModel
    
    template_name = 'post/post.html'
    context = {
        'siteTitle': 'Paylaşımlar',
    }
    
    def get(self, request):
        form = self.form_class()
        posts = self.model.objects.filter().order_by('-PublishDate')
        
        self.context.update({'form': form,
                             'posts': posts})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            FormSave = form.save(commit=False)
            FormSave.User = request.user
            FormSave.save()
            
        posts = self.model.objects.filter().order_by('-PublishDate')
        self.context.update({'form': form,
                             'posts': posts}) 
        return render(request, self.template_name, self.context)


def DeletePost(request, PostID):
    DeletePost = models.PostsModel.objects.get(id=PostID)
    
    if DeletePost.User == request.user:
        DeletePost.delete()
        
    return redirect('post')
    