from django.shortcuts import render
from django.views import View
from apps.blogs.forms import ArticleAddForm
from apps.blogs.models import ArticlesModel
# Create your views here.
class ArticleAddView(View):
    def get(self, request):
        form = ArticleAddForm()
        context = {
            'form': form,
        }
        return render(request, 'blogs/article-add.html', context)

    def post(self, request):
        form = ArticleAddForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
        context = {
            'form': form,
        }
        
        return render(request, 'blogs/article-add.html', context)

class ArticlesView(View):
    def get(self, request):
        articles = ArticlesModel.objects.all()

        context = {
            'articles':articles
        }
        return render(request, 'blogs/index.html', context)

class ArticlesDetailsView(View):
    def get(self, request, article_id):
        article = ArticlesModel.objects.filter(pk=article_id).first()

        context = {
            'article':article
        }
        return render(request, 'blogs/article-details.html', context)
