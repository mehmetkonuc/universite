from django.shortcuts import render, redirect, get_object_or_404
from apps.questions.models import QuestionsModel, Category
from apps.questions.forms import QuestionsAddForm
from django.views import View
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.comments.views import CommentView
from django.contrib import messages

# Create your views here.
class QuestionsView(View):
    model_questions = QuestionsModel
    template = 'questions/index.html'
    context = {
        'siteTitle': 'Sorular',
    }

    def get(self, request):
        data = self.model_questions.objects.filter(is_published=True)
        self.context.update({
            'data':data
        })
        return render(request, self.template, self.context)


class MyQuestionsView(View):
    model_questions = QuestionsModel
    template = 'questions/my_questions.html'
    context = {
        'siteTitle': 'Sorular',
    }

    def get(self, request):
        data = self.model_questions.objects.filter(is_published=True, user=request.user)
        self.context.update({
            'data':data
        })
        return render(request, self.template, self.context)


class DraftQuestionsView(View):
    model_questions = QuestionsModel
    template = 'questions/draft_questions.html'
    context = {
        'siteTitle': 'Sorular',
    }

    def get(self, request):
        data = self.model_questions.objects.filter(is_published=False, user=request.user)
        self.context.update({
            'data':data
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