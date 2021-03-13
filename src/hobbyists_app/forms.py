from django.forms import ModelForm, Textarea
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from tempus_dominus.widgets import DateTimePicker


class CreateUser(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exlude = ['profile_pic']
        # widgets = {
        #     "discuss": Textarea(attrs={'cols': 5, 'rows': 3, 'placeholder': "Tuangkan opini anda disini", 'class': 'input-komentar'}),
        # }


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


class FormEvent(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
                "format": "YYYY-MM-DD HH:mm:ss",


                # Calendar and time widget formatting
                'time': 'fa fa-clock-o',
                'date': 'fa fa-calendar',
                'up': 'fa fa-arrow-up',
                'down': 'fa fa-arrow-down',
                'previous': 'fa fa-chevron-left',
                'next': 'fa fa-chevron-right',
                'today': 'fa fa-calendar-check-o',
                'clear': 'fa fa-delete',
                'close': 'fa fa-times'
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    end_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
                "format": "YYYY-MM-DD HH:mm:ss",

                # Calendar and time widget formatting
                'time': 'fa fa-clock-o',
                'date': 'fa fa-calendar',
                'up': 'fa fa-arrow-up',
                'down': 'fa fa-arrow-down',
                'previous': 'fa fa-chevron-left',
                'next': 'fa fa-chevron-right',
                'today': 'fa fa-calendar-check-o',
                'clear': 'fa fa-delete',
                'close': 'fa fa-times'
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = ListEvent
        fields = '__all__'
        exclude = ['date_created', 'hadir', 'num_comment', 'num_hadir']
        widgets = {
            #     # 'user_id': forms.TextInput(attrs={'class': 'form-control', 'value': get_user_id()}),
            # 'start_time': forms.DateTimeInput(),
            'user_id': forms.TextInput(attrs={'type': 'hidden'}),
            # 'image': forms.TextInput(attrs={'type': 'hidden'}),
            #     # 'category': forms.ChoiceField(queryset=ListCategory.objects.all().order_by('name')),
            #     'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'id': 'descVal'}),
        }


class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email']
        # exclude = ['profile_pic']
        widgets = {
            # 'user_id': forms.TextInput(attrs={'class': 'form-control', 'value': get_user_id()}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'id': 'password', 'type': 'hidden'}),
        }

class FormUserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email']
        # exclude = ['profile_pic']
        # widgets = {
        #     # 'user_id': forms.TextInput(attrs={'class': 'form-control', 'value': get_user_id()}),
        #     'password': forms.TextInput(attrs={'class': 'form-control', 'id': 'password', 'type': 'hidden'}),
        # }


class FormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'hobby']
        # exclude = ['profile_pic']

class FormProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'hobby']
        # exclude = ['profile_pic']


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
