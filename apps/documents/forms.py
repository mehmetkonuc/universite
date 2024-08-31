from django import forms
from .models import DocumentsModel, DocumentsFolderModel

class FolderForm(forms.ModelForm):
    class Meta:
        model = DocumentsFolderModel
        fields = ['name']

class DocumentAddForm(forms.ModelForm):
    class Meta:
        model = DocumentsModel
        fields = ['folder', 'title', 'content']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Kullanıcıyı kwargs'tan alıyoruz
        super(DocumentAddForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['folder'].queryset = DocumentsFolderModel.objects.filter(user=user)