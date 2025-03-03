from django.shortcuts import render, redirect, get_object_or_404
from .models import DocumentsModel, DocumentsUploadModel, DocumentsFolderModel, UserDocumentsFilterModel
from .forms import DocumentAddForm, FolderForm, UserFilterForm
from django.views import View
from apps.likes.models import Likes
from apps.comments.views import CommentView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .filters import UserFilter, MyFilter
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin


class DocumentsView(View):
    model_data = DocumentsModel
    user_filter_model = UserDocumentsFilterModel
    filter_form = UserFilter
    user_filter_form = UserFilterForm
    template = 'documents/index.html'
    context = {'siteTitle': 'Dökümanlar'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        if request.user.is_authenticated:
            user_filter, created = self.user_filter_model.objects.get_or_create(user=request.user)
            # Apply filters
            filter = self.filter_form(model_to_dict(user_filter), queryset=data, request=request)
            filtered_data = filter.qs
        else:
            user_filter = {}
            filter = {}
            filtered_data = data

        # Apply sorting
        sorted_data = filtered_data
        
        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter,
            'user_filter': user_filter,
        })
        return render(request, self.template, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Misafir kullanıcılar için giriş sayfasına yönlendirme
        
        user_filter = self.user_filter_model.objects.get(user=request.user)

        if 'reset_filter' in request.POST:
            # Tüm filtre alanlarını temizle
            for field in model_to_dict(user_filter).keys():
                if field not in ['id', 'user']:  # user ve id hariç tüm alanları temizle
                    setattr(user_filter, field, None)
            user_filter.save()
            return self.get(request)  
        else:
            form = self.user_filter_form(request.POST, instance = user_filter)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.user=request.user
                form_data.save()
            data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
            data = data.annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count('comments', distinct=True)
        )
            filter = self.filter_form(data=request.POST, queryset=data, request=request)
            filtered_data = filter.qs
            # Apply sorting
            sorted_data = filtered_data
            
            # Pagination
            paginator = Paginator(sorted_data, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            self.context.update({
                'data': page_obj,
                'filter': filter,
                'user_filter': user_filter,
            })
            return render(request, self.template, self.context)


class MyDocumentsView(LoginRequiredMixin, View):
    model_data = DocumentsModel
    filter_form = MyFilter
    template = 'documents/my.html'
    context = {'siteTitle': 'Dokümanlarım'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=True, user=request.user).order_by('-create_at')
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        # Apply filters
        if 'reset_filter' in request.GET:
            filter = self.filter_form(queryset=data)
        else:
            filter = self.filter_form(request.GET, queryset=data)
            
        filtered_data = filter.qs
        
        # Apply sorting
        sorted_data = filtered_data
        
        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter,
        })
        return render(request, self.template, self.context)


class MyDraftDocumentsView(LoginRequiredMixin, View):
    model_data = DocumentsModel
    filter_form = MyFilter
    template = 'documents/draft.html'
    context = {'siteTitle': 'Taslaklarım'}
    paginate_by = 4

    def get(self, request):
        data = self.model_data.objects.filter(is_published=False, user=request.user).order_by('-create_at')
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )  
        # Apply filters
        if 'reset_filter' in request.GET:
            filter = self.filter_form(queryset=data)
        else:
            filter = self.filter_form(request.GET, queryset=data)

        filtered_data = filter.qs
        
        # Apply sorting
        sorted_data = filtered_data
        
        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'data': page_obj,
            'filter': filter,
        })
        return render(request, self.template, self.context)


class MyFoldersView(LoginRequiredMixin, View):
    def get(self, request):
        data = DocumentsFolderModel.objects.filter(user=request.user)
        context = {'data':data}
        
        return render(request, 'documents/my_folders.html', context)


class MyFoldersDetailsView(View):
    model_data = DocumentsModel
    filter_form = MyFilter
    template = 'documents/my_folder_details.html'
    context = {'siteTitle': 'Dokümanlarım'}
    paginate_by = 4

    def get(self, request, folder):
        data = DocumentsModel.objects.filter(folder_id=folder).order_by('-create_at')
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        # Apply filters
        if 'reset_filter' in request.GET:
            filter = self.filter_form(queryset=data)
        else:
            filter = self.filter_form(request.GET, queryset=data)

        filtered_data = filter.qs
        
        # Apply sorting
        sorted_data = filtered_data

        # Pagination
        paginator = Paginator(sorted_data, self.paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        folder = DocumentsFolderModel.objects.filter(id=folder).first()
        self.context.update({
            'data': page_obj,
            'filter': filter,
            'folder': folder,
        })
        
        return render(request, 'documents/my_folder_details.html', self.context)


class FolderAddView(LoginRequiredMixin, View):
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


class FolderEditView(LoginRequiredMixin, View):
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
    
    
class DocumentsAddView(LoginRequiredMixin, View):
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
        

class DocumentsEditView(LoginRequiredMixin, View):
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
    model_likes = Likes
    template = 'documents/details.html'
    paginate_by = 2
    context = {
        }

    def get(self, request, slug):
        data = get_object_or_404(self.model_document, slug=slug)
        comments =CommentView.comment_get(content_type=ContentType.objects.get_for_model(data), object_id=data.id)
        if request.user.is_authenticated:
            liked = data.likes.filter(user=request.user)
            liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)
        else:
            liked = {}
            liked_comment = {}

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        self.context.update({
            'siteTitle':data.title,
            'data': data,
            'comments': page_obj,
            'liked' : liked,
            'liked_comment' : liked_comment,
        })

        return render(request, self.template, self.context)

    def post(self, request, slug):
        data = get_object_or_404(self.model_document, slug=slug)
        form = CommentView.comment_post(request=request, content_type=ContentType.objects.get_for_model(data), object_id=data.id)
        liked = data.likes.filter(user=request.user)
        comments =CommentView.comment_get(content_type=ContentType.objects.get_for_model(data), object_id=data.id)
        liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        # content_type = ContentType.objects.get_for_model(data)
        # liked = self.model_likes.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)
        # comments =CommentView.comment_get(content_type=content_type, object_id=data.id)
        # liked_comment = self.model_likes.objects.filter(content_type=ContentType.objects.get_for_model(CommentView.model_comments), user=request.user).values_list('object_id', flat=True)

        paginator = Paginator(comments, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.context.update({
            'form': form,
            'data' : data,
            'comments': page_obj,
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