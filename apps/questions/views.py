from django.shortcuts import render, redirect, get_object_or_404
from apps.questions.models import QuestionsModel, Category
from apps.photos.models import PhotosModel
from apps.questions.forms import QuestionsAddForm
from django.views import View
from django.contrib.contenttypes.models import ContentType
from apps.likes.models import Like
from apps.comments.views import CommentView

# Create your views here.
class QuestionsView(View):
    model_questions = QuestionsModel
    template = 'questions/index.html'
    context = {
        'siteTitle': 'Sorular',
    }

    def get(self, request):
        data = self.model_questions.objects.all()

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
    model_photos = PhotosModel
    form_questions = QuestionsAddForm
    template = 'questions/add.html'
    context = {
        'siteTitle': 'Soru Ekle',
    }

    def get(self, request):
        form = self.form_questions()
        categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'categories' : categories
        })
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_questions(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            futured_images = request.FILES.get('futured_image')
            self.model_photos.objects.create(
                user=request.user,
                content_type=ContentType.objects.get_for_model(form_data),
                object_id=form_data.pk,
                photo=futured_images
            )
            return redirect('article_details', slug=form_data.slug)

        categories = self.model_categories.objects.filter(parent__isnull=True)

        self.context.update({
            'form': form,
            'categories' : categories
        })

        return render(request, self.template, self.context)