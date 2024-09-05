from django.shortcuts import render, redirect, get_object_or_404
from .models import QuestionsModel, Category, UserQuestionsFilterModel
from .forms import QuestionsAddForm, UserFilterForm
from .filters import UserFilter, MyFilter
from django.views import View
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.contrib import messages
from django.db.models import Count
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

# Create your views here.
class QuestionsView(View):
    model_data = QuestionsModel
    user_filter_model = UserQuestionsFilterModel
    filter_form = UserFilter
    user_filter_form = UserFilterForm
    template = 'questions/index.html'
    context = {'siteTitle': 'Sorular'}
    paginate_by = 4

    def get(self, request):
        user_filter, created = self.user_filter_model.objects.get_or_create(user=request.user)
        data = self.model_data.objects.filter(is_published=True).order_by('-create_at')
        # Annotate with like_count and comment_count
        data = data.annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True)
        )
        
        # Apply filters
        filter = self.filter_form(model_to_dict(user_filter), queryset=data)
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
    
    def post(self, request):
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
            filter = self.filter_form(data=request.POST, queryset=data)
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


class MyQuestionsView(View):
    model_data = QuestionsModel
    filter_form = MyFilter
    template = 'questions/my.html'
    context = {'siteTitle': 'Sorularım'}
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


class DraftQuestionsView(View):
    model_data = QuestionsModel
    filter_form = MyFilter
    template = 'questions/draft.html'
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


class QuestionsDetailsView(View):
    model_questions = QuestionsModel
    model_likes = Like
    template = 'questions/details.html'
    context = {
        }

    def get(self, request, slug):
        data = get_object_or_404(self.model_questions, slug=slug)
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
        data = get_object_or_404(self.model_questions, slug=slug)
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


class QuestionsAddView(View):
    model_categories = Category
    form_questions = QuestionsAddForm
    template = 'questions/add.html'
    context = {
        'siteTitle': 'Soru Ekle',
    }

    def get(self, request):
        form = self.form_questions()
        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_questions(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()

            return redirect('question_details', slug=form_data.slug)

        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
        })

        return render(request, self.template, self.context)


class QuestionsEditView(View):
    model_questions = QuestionsModel
    model_categories = Category
    form_questions = QuestionsAddForm
    template = 'questions/add.html'
    context = {
        'siteTitle': 'Soru Düzenle',
    }

    def get(self, request, slug):
        instance = self.model_questions.objects.filter(slug=slug).first()
        form = self.form_questions(instance=instance)
        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
        })
        return render(request, self.template, self.context)

    def post(self, request, slug):
        instance = self.model_questions.objects.filter(slug=slug).first()
        form = self.form_questions(request.POST, instance=instance)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()

            return redirect('question_details', slug=form_data.slug)

        # categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            # 'categories' : categories
        })

        return render(request, self.template, self.context)
    

def delete_questions(request, slug):
    delete = QuestionsModel.objects.get(slug=slug)

    if delete.user == request.user or request.user.is_superuser:
        delete.delete()
        messages.success(request, 'Başarıyla silindi.')
    else:
        messages.success(request, 'Bir hata ile karşılaşıldı.')
        
    return redirect('questions')