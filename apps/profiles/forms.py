from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
import apps.profiles.models as models
import apps.inputs.models as inputsModel

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = models.ProfilePictureModel
        fields = ['profile_photo']


class ProfileEditForm(UserChangeForm):
    first_name = forms.CharField(label="Adınız", required=True)
    last_name = forms.CharField(label="Soyadınız", required=True)

    email = forms.EmailField(required=True)
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class EducationalInformationForm(forms.ModelForm):

    class Meta:
        model = models.EducationalInformationModel
        fields = ['country', 'university', 'department', 'status']


class PrivacyForm(forms.ModelForm):
    MESSAGE_PRIVACY_CHOICES = [
        ('nobody', 'Hiç Kimse'),
        ('followers', 'Sadece Takipçilerim'),
        ('everyone', 'Herkes')
    ]

    is_private = forms.BooleanField(label="Hesabı Gizle", help_text='Hesap gizliyken paylaşımlarınızı takipçileriniz dışında hiç kimse göremez.', required=False)
    message_privacy = forms.ChoiceField(choices=MESSAGE_PRIVACY_CHOICES, required=True, label='Mesaj Gizliliği', help_text='Size kimlerin mesaj atabileceğini seçiniz.')
    class Meta:
        model = models.PrivacyModel
        fields = ['is_private', 'message_privacy']



class AdditionalInformationForm(forms.ModelForm):
    GENDER_PRIVACY_CHOICES = [
        ('', 'Cinsiyet Seç'),
        ('women', 'Kadın'),
        ('man', 'Erkek')
    ]

    RELATIONSHIP_PRIVACY_CHOICES = [
        ('', 'İlişki Durumunu Seç'),
        ('no_relation', 'İlişkisi Yok'),
        ('yes_relation', 'İlişkisi Var'),
        ('married', 'Evli'),

    ]

    living_country = forms.ModelChoiceField(
        queryset=inputsModel.CountriesModel.objects.all(),
        label='Yaşadığınız Ülke',
        help_text ='Yaşadığınız Ülkeyi Seçiniz',
        empty_label='Ülke Seçin',
        required=False,
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )

    living_city = forms.ModelChoiceField(
        queryset=inputsModel.City.objects.all(),
        label='Yaşadığınız Şehir',
        help_text ='Yaşadığınız Şehri Seçiniz',
        empty_label='Şehir Seçin',
        required=False,
        widget= forms.Select(attrs={
            'class': 'selectpicker w-100',
            'data-style': 'btn-default',
            'data-live-search': 'true'
        }),
    )
    gender = forms.ChoiceField(choices=GENDER_PRIVACY_CHOICES, required=False, label='Cinsiyet', help_text='Lütfen cinsiyetinizi seçiniz.')
    relationship = forms.ChoiceField(choices=RELATIONSHIP_PRIVACY_CHOICES, required=False, label='İlişki Durumu', help_text='Lütfen ilişki durumunuzu seçiniz.')


    class Meta:
        model = models.AdditionalInformationModel
        fields = ['living_country', 'living_city', 'date_of_birth', 'gender', 'relationship', 'about']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date_of_birth': 'Doğum tarihi',
            'about' : 'Hakkınızda'

        }
        help_texts = {
            'date_of_birth': 'Doğum Tarihinizi Seçin',
            'about': 'Hakkınızda bilgiler girin.',
        }