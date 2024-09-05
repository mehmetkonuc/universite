from django import forms
from .models import DocumentsModel, DocumentsFolderModel, UserDocumentsFilterModel


class UserFilterForm(forms.ModelForm):
    class Meta:
        model=UserDocumentsFilterModel
        fields= ['country', 'university', 'department', 'status', 'sort_by' ]
        labels = {
            'category': 'Kategori',
        } 


class FolderForm(forms.ModelForm):
    class Meta:
        model = DocumentsFolderModel
        fields = ['name']

        labels = {
        'name': 'Klasör Adı',
    }
        help_texts = {
        'name': 'Klasörün adını yazınız..',
    }


class DocumentAddForm(forms.ModelForm):
    STATUS_CHOICES = [
        (False, 'Taslaklara Kaydet'),
        (True, 'Yayınla'),
    ]

    is_published = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
            }),
        required=True,
        help_text='Makalenin yayımlanmasını mı yoksa taslak olarak mı kaydedileceğini seçin.',
        initial = True,
        label = 'Yayınlama Durumu',
    )
    
    class Meta:
        model = DocumentsModel
        fields = ['folder', 'title', 'content', 'is_published']

        widgets = {
            'folder': forms.Select(attrs={
                'class': 'selectpicker w-100',
                'data-style': 'btn-default',
                'data-live-search': 'true'
            }),
        }
        labels = {
        'folder': 'Klasör',
        'title': 'Başlık',
        'content': 'Açıklama',
    }
        help_texts = {
        'folder': 'Klasör seçin veya oluşturun.',
        'title': 'Dökümanlarınıza uygun başlık girin. 150 harften fazla olamaz.',
        'content': 'Dökümanlarınızı açıklayınız.',
    }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Kullanıcıyı kwargs'tan alıyoruz
        super(DocumentAddForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['folder'].queryset = DocumentsFolderModel.objects.filter(user=user)