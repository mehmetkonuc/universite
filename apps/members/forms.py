from django import forms
from .models import MembersFilterModel


class UserFilterForm(forms.ModelForm):
    class Meta:
        model=MembersFilterModel
        fields= ['country', 'university', 'department', 'status']