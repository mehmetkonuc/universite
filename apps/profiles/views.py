from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.profiles import forms
from django.contrib.auth import logout
import apps.profiles.models as models
from django.contrib.auth import get_user_model
from apps.post.models import PostsModel
from apps.blogs.models import ArticlesModel
from apps.comments.models import Comment
from apps.likes.models import Like
from apps.marketplace.models import MarketPlaceModel
from apps.documents.models import DocumentsModel
from apps.confessions.models import ConfessionsModel
from apps.questions.models import QuestionsModel
from django.contrib.contenttypes.models import ContentType

class ProfileView(LoginRequiredMixin, View):
    model = models.EducationalInformationModel
    model_posts = PostsModel
    template = 'profiles/index.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(users, username=username)
        article = ArticlesModel.objects.filter(user=profile).count()
        comment = Comment.objects.filter(user=profile).count()
        like = Like.objects.filter(user=profile).count()
        posts = self.model_posts.objects.filter(User=profile).count()
        marketplace = MarketPlaceModel.objects.filter(user=profile).count()
        documents = DocumentsModel.objects.filter(user=profile).count()
        confessions = ConfessionsModel.objects.filter(user=profile, is_privacy=False).count()
        questions = QuestionsModel.objects.filter(user=profile).count()
        
        self.context.update(
            {'profile': profile,
            'article': article,
            'comment': comment,
            'marketplace': marketplace,
            'documents': documents,
            'confessions': confessions,
            'questions': questions,
            'like': like,
            'posts':posts}
        )
        return render(request, self.template, self.context)


class PostsProfileView(LoginRequiredMixin, View):
    model_posts = PostsModel
    model_like = Like
    template = 'profiles/posts.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(users, username=username)
        posts = self.model_posts.objects.filter(User=profile)
        content_type = ContentType.objects.get_for_model(self.model_posts)
        liked = self.model_like.objects.filter(content_type=content_type, user=request.user).values_list('object_id', flat=True)

        self.context.update(
            {'profile': profile,
             'posts':posts,
            'liked':liked
             }
        )
        return render(request, self.template, self.context)


class ArticlesProfileView(LoginRequiredMixin, View):
    model_articles = ArticlesModel
    template = 'profiles/articles.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(users, username=username)
        articles = self.model_articles.objects.filter(user=profile)

        self.context.update(
            {'profile': profile,
             'articles':articles,
             }
        )
        return render(request, self.template, self.context)


class MarketplaceProfileView(LoginRequiredMixin, View):
    model_marketplace = MarketPlaceModel
    template = 'profiles/marketplace.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(users, username=username)
        marketplace = self.model_marketplace.objects.filter(user=profile)

        self.context.update(
            {'profile': profile,
             'marketplace':marketplace,
             }
        )
        return render(request, self.template, self.context)

class DocumentsProfileView(LoginRequiredMixin, View):
    model_documents = DocumentsModel
    template = 'profiles/documents.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(users, username=username)
        documents = self.model_documents.objects.filter(user=profile)

        self.context.update(
            {'profile': profile,
             'documents':documents,
             }
        )
        return render(request, self.template, self.context)

class ProfileSettingsView(LoginRequiredMixin, View):
    form_class = forms.ProfilePictureForm
    profile_form = forms.ProfileEditForm
    template_name = 'profiles/settings/profile-settings.html'
    context = {
        'siteTitle': 'Hesap Ayarları',
    }
    def get(self, request, *args, **kwargs):
        profile_picture_instance = models.ProfilePictureModel.objects.filter(user=request.user).first()
        picture = self.form_class(instance=profile_picture_instance)
        profile = self.profile_form(instance=request.user)
        self.context.update({'picture': picture, 'profile' : profile})

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if 'remove_photo' in request.POST:
            profile = request.user.profilepicturemodel
            profile.profile_photo.delete(save=True)
            return redirect('profile_settings')
        profile_picture_instance = models.ProfilePictureModel.objects.filter(user=request.user).first()
        picture = self.form_class(request.POST, request.FILES, instance=profile_picture_instance)
        profile = self.profile_form(instance=request.user)
        if profile.is_valid():          
            profile.save()
            
        self.context.update({'picture': picture, 'profile' : profile})

        return render(request, self.template_name, self.context)


class PictureSettingsView(LoginRequiredMixin, View):
    form_class = forms.ProfilePictureForm
    profile_form = forms.ProfileEditForm
    template_name = 'profiles/settings/profile-settings.html'
    context = {
        'siteTitle': 'Hesap Ayarları',
    }

    def post(self, request, *args, **kwargs):
        profile_picture_instance = get_object_or_404(models.ProfilePictureModel, user=request.user)
        picture = self.form_class(request.POST, request.FILES, instance=profile_picture_instance)
        profile = self.profile_form(instance=request.user)

        if picture.is_valid():
            pictureDelete = request.user.profilepicturemodel
            pictureDelete.profile_photo.delete(save=True)
             
            profile_picture_instance = picture.save(commit=False)
            profile_picture_instance.user = request.user 
            profile_picture_instance.save()
            
        self.context.update({'picture': picture, 'profile' : profile})

        return render(request, self.template_name, self.context)


class EducationSettingsView(LoginRequiredMixin, View):
    template_name = 'profiles/settings/education-settings.html'
    model = models.EducationalInformationModel
    form = forms.EducationalInformationForm
    context = {
        'siteTitle': 'Eğitim Ayarları',
    }
    def get(self, request):
        instance = self.model.objects.filter(User = request.user).first()
        form = self.form(instance=instance) if instance else self.form()

        self.context.update({'form': form,})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        instance = self.model.objects.filter(User = request.user).first()
        form = self.form(request.POST, instance=instance) if instance else self.form(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.User = request.user
            form_save.save()
        self.context.update({'form': form,})

        return render(request, self.template_name, self.context)


class AdditionalInformationView(LoginRequiredMixin, View):
    template_name = 'profiles/settings/additional-information.html'
    model = models.AdditionalInformationModel
    form = forms.AdditionalInformationForm
    context = {
        'siteTitle': 'Ek Bilgiler',
    }
    def get(self, request):
        instance = self.model.objects.filter(User = request.user).first()
        form = self.form(instance=instance) if instance else self.form()

        self.context.update({'form': form,})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        instance = self.model.objects.filter(User = request.user).first()
        form = self.form(request.POST, instance=instance) if instance else self.form(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.User = request.user
            form_save.save()
        self.context.update({'form': form,})

        return render(request, self.template_name, self.context)


class ProfileDeleteView(LoginRequiredMixin, View):
    template_name = 'profiles/settings/profile-delete.html'
    context = { 
            'siteTitle' : 'Hesabı Sil'           
        }
    def get(self, request):
        

        return render(request, self.template_name, self.context)
    
    def post(self, request):
        if request.POST['accountActivation'] == 'on':
            user = request.user
            user.delete()
            logout(request)
            return redirect('home')
        else:
            return render(request, self.template_name)