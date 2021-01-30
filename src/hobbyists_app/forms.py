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
            'topic': forms.TextInput(attrs={'class': 'form-control', 'id': 'topicVal'}),
            'user_id': forms.TextInput(attrs={'type': 'hidden'}),
            # 'category': forms.ChoiceField(queryset=ListCategory.objects.all().order_by('name')),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'id': 'descVal'}),
        }


class FormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['profile_pic']
        # widgets = {
        #     # 'user_id': forms.TextInput(attrs={'class': 'form-control', 'value': get_user_id()}),
        #     'topic': forms.TextInput(attrs={'class': 'form-control', 'id': 'topicVal'}),
        #     'user_id': forms.TextInput(attrs={'type': 'hidden'}),
        #     # 'category': forms.ChoiceField(queryset=ListCategory.objects.all().order_by('name')),
        #     'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'id': 'descVal'}),
        # }


class updateLikeForm(forms.ModelForm):
    class Meta:
        model = ListForum
        fields = ['num_like']


class CreateInDiscussion(ModelForm):
    class Meta:
        model = ForumDiscussion
        fields = ['discuss', 'user_id', 'forum_id']
        widgets = {
            "discuss": Textarea(attrs={'cols': 5, 'rows': 3, 'placeholder': "Tuangkan opini anda disini", 'class': 'input-komentar'}),
        }
