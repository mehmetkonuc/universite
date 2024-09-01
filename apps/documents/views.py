from django.shortcuts import render, redirect, get_object_or_404
from .models import DocumentsModel, DocumentsUploadModel, DocumentsFolderModel
from .forms import DocumentAddForm, FolderForm
from django.views import View
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


class DocumentsView(View):
    def get(self, request):
        data = DocumentsModel.objects.filter(is_published=True)
        context = {'data':data}
        
        return render(request, 'documents/index.html', context)


class MyDocumentsView(View):
    def get(self, request):
        data = DocumentsModel.objects.filter(user=request.user, is_published = True)
        context = {'data':data}
        
        return render(request, 'documents/my_documents.html', context)


class MyDraftDocumentsView(View):
    def get(self, request):
        data = DocumentsModel.objects.filter(user=request.user, is_published = False)
        context = {'data':data}
        
        return render(request, 'documents/my_draft_documents.html', context)


class MyFoldersView(View):
    def get(self, request):
        data = DocumentsFolderModel.objects.filter(user=request.user)
        context = {'data':data}
        
        return render(request, 'documents/my_folders.html', context)


class MyFoldersDetailsView(View):
    def get(self, request, folder):
        data = DocumentsModel.objects.filter(user=request.user, folder_id=folder)
        folder = DocumentsFolderModel.objects.filter(id=folder).first()
        context = {'data':data,
                   'folder':folder}
        
        return render(request, 'documents/my_folder_details.html', context)


class FolderAddView(View):
    model_folder = DocumentsFolderModel
    form_class = FolderForm
    template = 'documents/folder_add.html'
    context = {
        'siteTitle' : 'Klasör Oluştur'
    }
    
    def get(self, request):
        form = self.form_class()
        self.context.update({
            'form':form
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('my_folders')
        
        self.context.update({
            'form':form
        })
        return render(request, self.template, self.context)


class FolderEditView(View):
    model_folder = DocumentsFolderModel
    form_class = FolderForm
    template = 'documents/folder_add.html'
    context = {
        'siteTitle' : 'Klasör Oluştur'
    }
    
    def get(self, request, folder_id):
        instance = self.model_folder.objects.filter(id=folder_id).first()
        form = self.form_class(instance=instance)
        self.context.update({
            'form':form
        })
        return render(request, self.template, self.context)

    def post(self, request, folder_id):
        instance = self.model_folder.objects.filter(id=folder_id).first()
        form = self.form_class(data=request.POST, instance=instance)
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('my_folder_details', folder_id )
        
        self.context.update({
            'form':form
        })
        return render(request, self.template, self.context)
    
    
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
        form = self.form_class(request.POST, user=request.user)
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
            if form_data.is_published:
                messages.success(request, 'Başarıyla yayınlandı.')
            else:
                messages.success(request, 'Başarıyla taslaklara kaydedildi.')
                
            return redirect('document_details', slug=form_data.slug)

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
        form = self.form_class(instance=instance, user=request.user)
        form_folder = self.form_folder()
        
        self.context.update({
            'form':form,
            'form_folder':form_folder,
            'instance':instance
        })
        return render(request, self.template, self.context)

    def post(self, request, slug):
        instance = get_object_or_404(self.model_documents, slug=slug)
        form = self.form_class(data=request.POST, instance=instance, user=request.user)
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
            if form_data.is_published:
                messages.success(request, 'Başarıyla düzenlendi ve yayınlandı.')
            else:
                messages.success(request, 'Başarıyla düzenlendi ve taslaklara kaydedildi.')
            
            return redirect('document_details', slug=form_data.slug)

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
            'data': data,
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


def delete_folder(request, folder_id):
    delete = DocumentsFolderModel.objects.get(id=folder_id)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()
        messages.success(request, 'Başarıyla silindi.')
        
    return redirect('my_folders')