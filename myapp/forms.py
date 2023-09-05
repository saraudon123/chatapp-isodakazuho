from dataclasses import fields
from pyexpat import model
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
    keyword = forms.CharField(max_length=20, label="名前で検索", required=False)