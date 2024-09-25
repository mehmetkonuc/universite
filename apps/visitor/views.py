from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from . import forms
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.profiles.models import ProfilePictureModel, PrivacyModel , EducationalInformationModel
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

def register_step1(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            # Form bilgilerini oturumda sakla
            request.session['register_data'] = form.cleaned_data
            return redirect('register_step2')
    else:
        form = forms.RegisterForm()
    
    return render(request, 'visitor/register.html', {'form': form})

def register_step2(request):
    if 'register_data' not in request.session:
        return redirect('register')  # Eğer oturum verisi yoksa ilk adıma geri dön

    if request.method == 'POST':
        form = forms.EducationalInformationForm(request.POST)
        if form.is_valid():
            # Oturumda saklanan kullanıcı verisini al
            user_data = request.session.get('register_data')

            # Geçici kullanıcıyı oluştur
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password1']  # password1 doğrulandı
            )
            
            # Educational Information kaydet
            educational_info = form.save(commit=False)
            educational_info.user = user
            educational_info.save()

            #Hesap Gizliliğini Önceden Ayarla
            PrivacyModel.objects.get_or_create(user=user)
            
            # Kullanıcı oturumu aç
            login(request, user)
            
            # Oturumdan kullanıcı verisini temizle
            del request.session['register_data']
            
            return redirect('home')  # Profil sayfasına yönlendirin
    
    else:
        form = forms.EducationalInformationForm()

    return render(request, 'visitor/register.html', {'form': form})


def profile_photo(request):
    profile_picture, created = ProfilePictureModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = forms.ProfilePictureForm(request.POST, request.FILES, instance=profile_picture)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('profile', profile_picture.user.username)

    return render(request, 'visitor/profile_photo.html')


# Create your views here.
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
    return render(request, 'visitor/login.html', context)


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