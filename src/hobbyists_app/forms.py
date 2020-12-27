from django.forms import ModelForm, Textarea
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class FormForum(forms.ModelForm):
    class Meta:
        model = ListForum
        fields = '__all__'
        exclude = ['date_created', 'num_like', 'num_comment']
        widgets = {
            # 'user_id': forms.TextInput(attrs={'class': 'form-control', 'value': get_user_id()}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
