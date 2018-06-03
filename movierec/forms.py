from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']                
        widgets = {
            'username': forms.TextInput(attrs={'class': 'mdl-textfield__input','id':'id_username'}),
            'email': forms.TextInput(attrs={'class': 'mdl-textfield__input','id':'id_email','type':'email' }),
            'password': forms.TextInput(attrs={'class': 'mdl-textfield__input','id':'id_password'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)
    