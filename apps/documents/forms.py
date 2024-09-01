from django import forms
from .models import DocumentsModel, DocumentsFolderModel

class FolderForm(forms.ModelForm):
    class Meta:
        model = DocumentsFolderModel
        fields = ['name']

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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Kullanıcıyı kwargs'tan alıyoruz
        super(DocumentAddForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['folder'].queryset = DocumentsFolderModel.objects.filter(user=user)