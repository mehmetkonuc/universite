from django.shortcuts import render, redirect, get_object_or_404
from .models import FolderModel, DocumentsModel
from .forms import FolderForm, DocumentForm
from django.views import View
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.contrib.contenttypes.models import ContentType

def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
    else:
        form = FolderForm()
    return render(request, 'documents/create_folder.html', {'form': form})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
    else:
        form = DocumentForm()
    return render(request, 'documents/upload_document.html', {'form': form})

class DocumentsView(View):
    def get(self, request):
        data = DocumentsModel.objects.all()
        context = {'data':data}
        
        return render(request, 'documents/index.html', context)

class DocumentDetailsView(View):
    model_document = DocumentsModel
    model_likes = Like
    template = 'documents/details.html'
    context = {
        }

    def get(self, request, slug):
        data = get_object_or_404(self.model_document, slug=slug)
        content_type = ContentType.objects.get_for_model(data)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'siteTitle':data.title,
            'document': data,
            'comments': comments,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        data = get_object_or_404(self.model_document, slug=slug)
        content_type = ContentType.objects.get_for_model(data)
        form = CommentView.comment_post(request=request, content_type=content_type, object_id=data.id)
        liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        comments =CommentView.comment_get(content_type=content_type, object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        self.context.update({
            'form': form,
            'data' : data,
            'comments': comments,
            'liked' : liked,
            'liked_comment' : liked_comment,
            })
        return render(request, self.template, self.context)
