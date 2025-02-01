from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.profiles import forms
from django.contrib.auth import logout
import apps.profiles.models as models
from django.contrib.auth import get_user_model
from apps.likes.models import Likes
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from apps.post.models import PostsModel

def profile_photo(request):
    profile_picture, created = models.ProfilePictureModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = forms.ProfilePictureForm(request.POST, request.FILES, instance=profile_picture)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('profile', profile_picture.user.username)

    return render(request, 'profiles/settings/profile_photo.html')


class ProfileView(LoginRequiredMixin, View):
    model = models.EducationalInformationModel
    template = 'profiles/index.html'
    context = {
    }

    def get(self, request, username):
        # Tek sorguda profile ile ilişkili user ve educational information verilerini çekiyoruz
        users = get_user_model()
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'additional_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'comments',
                'likes',
                'posts',
                'blogs',
                'marketplace',
                'documents',
                'questions',
                'confessions',
            ), 
            username=username
        )

        # # İtiraf sayısını alıyoruz
        # confessions = ConfessionsModel.objects.filter(user=profile, is_privacy=False).count()

        # Profil ile ilişkili takipçi ve takip isteklerini alıyoruz
        followers = profile.followers.filter(follower=request.user)
        follow_requests = profile.follow_requests_received.filter(follower=request.user)

        self.context.update({
            'profile': profile,
            'followers': followers,
            'follow_requests': follow_requests,
        })
        return render(request, self.template, self.context)


class FollowersProfileView(LoginRequiredMixin, View):
    # model_marketplace = MarketPlaceModel
    template = 'profiles/followers.html'
    paginate_by = 12
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
            ), 
            username=request.user.username
        )
        # marketplace = self.model_marketplace.objects.filter(user=profile, is_published = True)
        followers = profile.followers.all()

        # marketplace = profile.marketplace.filter(is_published = True)
        paginator = Paginator(followers, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # followers = profile.followers.filter(follower=request.user)

        self.context.update(
            {
            'siteTitle' : str(profile.first_name) + ' ' + str(profile.last_name) + ' - ' + 'Takipçileri',
            'profile': profile,
            'data':page_obj,
            #  'followers':followers,
             }
        )
        return render(request, self.template, self.context)


class FollowingProfileView(LoginRequiredMixin, View):
    # model_marketplace = MarketPlaceModel
    template = 'profiles/following.html'
    paginate_by = 12
    context = {
    }

    def get(self, request):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'profile_photo',
            ).prefetch_related(
                'followers', 
                'following', 
            ), 
            username=request.user.username
        )

        following = profile.following.all()

        # marketplace = profile.marketplace.filter(is_published = True)
        paginator = Paginator(following, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # followers = profile.followers.filter(follower=request.user)

        self.context.update(
            {
            'siteTitle' : str(profile.first_name) + ' ' + str(profile.last_name) + ' - ' + 'Takip Ettikleri',
            'profile': profile,
            'data':page_obj,
             }
        )
        return render(request, self.template, self.context)


class PostsProfileView(LoginRequiredMixin, View):
    model_like = Likes
    model_posts = PostsModel
    paginate_by = 12
    template = 'profiles/posts.html'
    context = {}

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'posts',
            ), 
            username=username
        )

        # posts ve ilişkili yorumlar, beğeniler
        posts = profile.posts.all().order_by('-create_at').prefetch_related('likes', 'comments')

        # Sayfalama işlemi
        paginator = Paginator(posts, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Zaten page_obj'de postların ID'leri var, bunları kullanarak beğenilenleri alalım
        post_ids = page_obj.object_list.values_list('id', flat=True)

        # Kullanıcının beğendiği post'ları toplu olarak tek sorguda alıyoruz
        content_type = ContentType.objects.get_for_model(self.model_posts)
        liked = self.model_like.objects.filter(
            content_type=content_type, user=request.user, object_id__in=post_ids
        ).values_list('object_id', flat=True)
        
        # Kullanıcının takip ettiği kullanıcılar
        followers = profile.followers.filter(follower=request.user)

        # Context verilerini güncelle
        self.context.update({
            'siteTitle': f'{profile.first_name} {profile.last_name} - Gönderileri',
            'profile': profile,
            'data': page_obj,
            'liked': liked,
            'followers': followers
        })

        return render(request, self.template, self.context)


class ArticlesProfileView(LoginRequiredMixin, View):
    # model_articles = ArticlesModel
    template = 'profiles/articles.html'
    paginate_by = 12
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'blogs',
            ), 
            username=username
        )

        articles = profile.blogs.filter(is_published = True).order_by('-create_at').prefetch_related('likes', 'comments')

        paginator = Paginator(articles, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        followers = profile.followers.filter(follower=request.user)

        self.context.update({
            'siteTitle': f'{profile.first_name} {profile.last_name} - Makaleleri',
            'profile': profile,
            'data':page_obj,
            'followers':followers
        })

        return render(request, self.template, self.context)


class MarketplaceProfileView(LoginRequiredMixin, View):
    # model_marketplace = MarketPlaceModel
    template = 'profiles/marketplace.html'
    paginate_by = 12
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'marketplace',
            ), 
            username=username
        )

        marketplace = profile.marketplace.filter(is_published = True).order_by('-create_at')

        paginator = Paginator(marketplace, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        followers = profile.followers.filter(follower=request.user)

        self.context.update({
            'siteTitle': f'{profile.first_name} {profile.last_name} - İlanları',
            'profile': profile,
            'data':page_obj,
            'followers':followers,
        })
        
        return render(request, self.template, self.context)


class DocumentsProfileView(LoginRequiredMixin, View):
    # model_documents = DocumentsModel
    template = 'profiles/documents.html'
    paginate_by = 12
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'documents',
            ), 
            username=username
        )

        documents = profile.documents.filter(is_published = True).order_by('-create_at').prefetch_related('likes', 'comments')

        paginator = Paginator(documents, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        followers = profile.followers.filter(follower=request.user)

        self.context.update({
            'siteTitle': f'{profile.first_name} {profile.last_name} - Dokümanları',
            'profile': profile,
            'data':page_obj,
            'followers':followers
        })

        return render(request, self.template, self.context)


class ConfessionsProfileView(LoginRequiredMixin, View):
    template = 'profiles/confessions.html'
    paginate_by = 12
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'confessions',
            ), 
            username=username
        )

        confessions = profile.confessions.filter(is_privacy = False, is_published = True).prefetch_related('likes', 'comments')

        paginator = Paginator(confessions, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        followers = profile.followers.filter(follower=request.user)

        self.context.update({
            'siteTitle': f'{profile.first_name} {profile.last_name} - İtirafları',
            'profile': profile,
            'data':page_obj,
            'followers':followers,
        })

        return render(request, self.template, self.context)


class QuestionsProfileView(LoginRequiredMixin, View):
    template = 'profiles/questions.html'
    paginate_by = 12
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        profile = get_object_or_404(
            users.objects.select_related(
                'educational_information', 
                'privacy', 
                'profile_photo'
            ).prefetch_related(
                'followers', 
                'following', 
                'follow_requests_received', 
                'questions',
            ), 
            username=username
        )

        questions = profile.questions.filter(is_published = True).prefetch_related('likes', 'comments')

        paginator = Paginator(questions, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        followers = profile.followers.filter(follower=request.user)

        self.context.update({
            'siteTitle': f'{profile.first_name} {profile.last_name} - Soruları',
            'profile': profile,
            'data':page_obj,
            'followers':followers,
        })
        
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
            try:
                photo = request.user.profile_photo
                photo.delete()
            except:
                pass
            return redirect('profile_settings')
        profile_picture_instance = models.ProfilePictureModel.objects.filter(user=request.user).first()
        picture = self.form_class(request.POST, request.FILES, instance=profile_picture_instance)
        profile = self.profile_form(request.POST, instance=request.user)
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
            pictureDelete = request.user.profile_photo
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
        instance = self.model.objects.filter(user = request.user).first()
        form = self.form(instance=instance) if instance else self.form()

        self.context.update({'form': form,})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        instance = self.model.objects.filter(user = request.user).first()
        form = self.form(request.POST, instance=instance) if instance else self.form(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
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
        instance = self.model.objects.filter(user = request.user).first()
        form = self.form(instance=instance) if instance else self.form()

        self.context.update({'form': form,})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        instance = self.model.objects.filter(user = request.user).first()
        form = self.form(request.POST, instance=instance) if instance else self.form(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
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


class PrivacyView(LoginRequiredMixin, View):
    model = models.PrivacyModel
    form_class = forms.PrivacyForm
    template_name = 'profiles/settings/privacy.html'
    context = {

    }

    def get(self, request):
        instance = self.model.objects.filter(user = request.user).first()
        form = self.form_class(instance=instance) if instance else self.form_class()
        self.context.update({'form': form,})

        return render(request, self.template_name, self.context)
    
    def post(self, request):
        instance = self.model.objects.filter(user = request.user).first()
        form = self.form_class(data=request.POST, instance=instance) if instance else self.form_class(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            
        self.context.update({'form': form,})

        return render(request, self.template_name, self.context)
