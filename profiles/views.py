from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth import logout
import profiles.models as models

class ProfileSettingsView(LoginRequiredMixin, View):
    template_name = 'profile/profileSettings.html'
    context = {
        'siteTitle': 'Hesap Ayarları',
    }

    def get(self, request):
        user = request.user
        form = forms.ProfileEditForm(instance=user)

        self.context.update({'form': form,})
        
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = forms.ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        self.context.update({'form': form,})

        return render(request, self.template_name, self.context)


class EducationSettingsView(LoginRequiredMixin, View):
    template_name = 'profile/EducationSettings.html'
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
            FormSave = form.save(commit=False)
            FormSave.User = request.user
            FormSave.save()
        self.context.update({'form': form,})

        return render(request, self.template_name, self.context)


class ProfileDeleteView(LoginRequiredMixin, View):
    template_name = 'profile/profileDelete.html'
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


class ProfileView(LoginRequiredMixin, View):
    model = models.EducationalInformationModel
    template = 'profile/profile.html'
    context = {
        'siteTitle' : 'Profil',
    }

    def get(self, request):
        model = self.model.objects.filter(User=request.user).first()
        self.context.update(
            {'model': model,}
        )
        return render(request, self.template, self.context)