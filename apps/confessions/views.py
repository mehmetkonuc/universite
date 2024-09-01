from django.shortcuts import render, get_object_or_404, redirect
from apps.confessions.models import ConfessionsModel
from apps.photos.models import PhotosModel
from apps.confessions.forms import ConfessionsForm
from django.views import View
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.contrib import messages

# Create your views here.
class ConfessionsView(View):
    model_confessions = ConfessionsModel
    template = 'confessions/index.html'
    context = {
        'siteTitle': 'İtiraflar',
    }

    def get(self, request):
        confessions = self.model_confessions.objects.filter(is_published=True).order_by('-create_at')

        self.context.update({
            'data':confessions
        })
        return render(request, self.template, self.context)


class MyConfessionsView(View):
    model_confessions = ConfessionsModel
    template = 'confessions/my_confessions.html'
    context = {
        'siteTitle': 'İtiraflar',
    }

    def get(self, request):
        confessions = self.model_confessions.objects.filter(user=request.user, is_published=True).order_by('-create_at')
        self.context.update({
            'data':confessions
        })
        return render(request, self.template, self.context)


class MyDraftConfessionsView(View):
    model_confessions = ConfessionsModel
    template = 'confessions/my_confessions.html'
    context = {
        'siteTitle': 'İtiraflar',
    }

    def get(self, request):
        confessions = self.model_confessions.objects.filter(user=request.user, is_published=False).order_by('-create_at')
        self.context.update({
            'data':confessions
        })
        return render(request, self.template, self.context)


class ConfessionDetailView(View):
    model_confessions = ConfessionsModel
    model_likes = Like
    template = 'confessions/details.html'
    context = {
        }

    def get(self, request, slug):
        confession = get_object_or_404(self.model_confessions, slug=slug)
        content_type = ContentType.objects.get_for_model(confession)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=confession.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'siteTitle':confession.title,
            'data': confession,
            'comments': comments,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        confession = get_object_or_404(self.model_confessions, slug=slug)
        content_type = ContentType.objects.get_for_model(confession)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=confession.id)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=confession.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'form': form,
            'data' : confession,
            'comments': comments,
            'liked' : liked,
            'liked_comment' : liked_comment,
            })
        return render(request, self.template, self.context)

class ConfessionsAddView(View):
    model_confessions = ConfessionsModel
    model_photos = PhotosModel
    form_confessions = ConfessionsForm
    template = 'confessions/add.html'
    context = {
        'siteTitle': 'İtiraf Ekle',
    }

    def get(self, request):
        initial = request.user.educationalinformationmodel.University
        form = self.form_confessions(initial = {'university' : initial})

        self.context.update({
            'form': form,
        })
        return render(request, self.template, self.context)

    def post(self, request):
        initial = request.user.educationalinformationmodel.University
        form = self.form_confessions(request.POST, initial = {'university' : initial})

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('confession_details', slug=form_data.slug)


        self.context.update({
            'form': form,
        })

        return render(request, self.template, self.context)


class ConfessionsEditView(View):
    model_confessions = ConfessionsModel
    model_photos = PhotosModel
    form_confessions = ConfessionsForm
    template = 'confessions/add.html'
    context = {
        'siteTitle': 'İtiraf Düzenle',
    }

    def get(self, request, slug):
        instance = self.model_confessions.objects.filter(slug=slug).first()
        form = self.form_confessions(instance = instance)

        self.context.update({
            'form': form,
        })
        return render(request, self.template, self.context)

    def post(self, request, slug):
        instance = self.model_confessions.objects.filter(slug=slug).first()

        form = self.form_confessions(request.POST, instance=instance)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('confession_details', slug=form_data.slug)


        self.context.update({
            'form': form,
        })

        return render(request, self.template, self.context)


def delete_confessions(request, confessions_id):
    delete = ConfessionsModel.objects.get(id=confessions_id)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()
        messages.success(request, 'Başarıyla silindi.')
    else:
        messages.success(request, 'Bir hata ile karşılaşıldı.')
        
    return redirect('confessions')