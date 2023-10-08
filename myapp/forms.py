from dataclasses import fields
from operator import mod
from pyexpat import model
from statistics import mode
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Talk


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'img')
    

class LoginForm(AuthenticationForm):
    pass

class TalkRoomForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('message',)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class FriendSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label="名前とメールアドレスで検索", required=False)

class ImageChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('img',)