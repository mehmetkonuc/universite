from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth import logout
import apps.profiles.models as models
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class ProfileView(LoginRequiredMixin, View):
    model = models.EducationalInformationModel
    template = 'profile.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request, username):
        users = get_user_model()  # Varsayılan kullanıcı modelini al
        user = get_object_or_404(users, username=username)
        model = self.model.objects.filter(User=user).first()
        self.context.update(
            {'model': model,
             'profileUser' : user}
        )
        return render(request, self.template, self.context)
    

class ProfileSettingsView(LoginRequiredMixin, View):
    form_class = forms.ProfilePictureForm
    profile_form = forms.ProfileEditForm
    template_name = 'settings/profile-settings.html'
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
    template_name = 'settings/profile-settings.html'
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
    template_name = 'settings/education-settings.html'
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
    template_name = 'settings/additional-information.html'
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
    template_name = 'settings/profile-delete.html'
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