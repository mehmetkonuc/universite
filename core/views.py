from django.views import View
from django.shortcuts import render, render, redirect
from . import forms
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404


def register_view(request):
    if request.user.is_authenticated:
        raise Http404("Sayfa bulunamadı")
    
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
    else:
        form = forms.RegisterForm()
    context = {
        'form': form,
        'siteTitle': 'Kayıt Ol'
    }
    return render(request, 'guest/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        raise Http404("Sayfa bulunamadı")
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = forms.LoginForm()

    context = {
        'form': form,
        'siteTitle': 'Giriş Yap'
    }
    return render(request, 'guest/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            form.add_error('email', ValidationError(
                "Bu e-posta adresi sistemde kayıtlı değil."))
            return self.form_invalid(form)
        return super().form_valid(form)


class Home(View):
    def get(self, request):

        return render(request, 'home.html')
