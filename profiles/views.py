from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth import logout


class ProfileSettingsView(LoginRequiredMixin, View):
    template_name = 'profile/profileSettings.html'
    context = {
        'siteTitle': 'Profili Düzenle',
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
            