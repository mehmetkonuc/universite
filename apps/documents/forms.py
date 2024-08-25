from django import forms
from .models import FolderModel, DocumentsModel

class FolderForm(forms.ModelForm):
    class Meta:
        model = FolderModel
        fields = ['name', 'parent']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentsModel
        fields = ['title', 'file', 'folder', 'content']