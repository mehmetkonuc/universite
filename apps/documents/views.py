from django.shortcuts import render, redirect, get_object_or_404
from .models import DocumentsModel, DocumentsUploadModel
from .forms import DocumentAddForm, FolderForm
from django.views import View
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


class DocumentsView(View):
    def get(self, request):
        data = DocumentsModel.objects.all()
        context = {'data':data}
        
        return render(request, 'documents/index.html', context)


class MyDocumentsView(View):
    def get(self, request):
        data = DocumentsModel.objects.filter(user=request.user)
        context = {'data':data}
        
        return render(request, 'documents/my_documents.html', context)


class DocumentsAddView(View):
    model_documents = DocumentsModel
    model_upload_documents = DocumentsUploadModel
    form_class = DocumentAddForm
    form_folder = FolderForm
    template = 'documents/add.html'
    context = {
        'siteTitle': 'Doküman Yükle'
    }
    def get(self, request):
        form = self.form_class(user=request.user)
        form_folder = self.form_folder()

        self.context.update({
            'form':form,
            'form_folder':form_folder,
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_class(request.POST)
        form_folder = self.form_folder()
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            documents = request.FILES.getlist('documents')
            for document in documents:
                self.model_upload_documents.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(form_data),
                    object_id=form_data.pk,
                    document=document
                )
        self.context.update({
            'form': form,
            'form_folder': form_folder,
        })
        return render(request, self.template, self.context)
        

class DocumentsEditView(View):
    model_documents = DocumentsModel
    model_upload_documents = DocumentsUploadModel
    form_class = DocumentAddForm
    form_folder = FolderForm
    template = 'documents/add.html'
    context = {
        'siteTitle': 'Doküman Yükle'
    }
    def get(self, request, slug):
        instance = get_object_or_404(self.model_documents, slug=slug)
        form = self.form_class(instance=instance)
        form_folder = self.form_folder()
        
        self.context.update({
            'form':form,
            'form_folder':form_folder,
            'instance':instance
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_class(request.POST)
        form_folder = self.form_folder()
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            documents = request.FILES.getlist('documents')
            for document in documents:
                self.model_upload_documents.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(form_data),
                    object_id=form_data.pk,
                    document=document
                )
        self.context.update({
            'form': form,
            'form_folder': form_folder,
        })
        return render(request, self.template, self.context)


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

def create_folder(request):
    form = FolderForm(request.POST)
    
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.user = request.user
        form_data.save()
        messages.success(request, 'Klasör başarıyla oluşturuldu.')

    else:
        messages.error(request, 'Klasör oluşturulamadı, lütfen tekrar deneyin.')

    return redirect('documents_add')


def delete_documents(request, docuements_id):
    delete = DocumentsModel.objects.get(id=docuements_id)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()

    return redirect('documents')