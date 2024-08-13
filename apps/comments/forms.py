from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']
    
    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        if parent:
            self.fields['parent'].initial = parent
            self.fields['parent'].widget = forms.HiddenInput()