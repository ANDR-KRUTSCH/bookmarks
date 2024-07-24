from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email')

    def clean_password2(self) -> str:
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data.get('password2')
    
    def clean_email(self) -> str:
        if self.cleaned_data.get('email') != '':
            if User.objects.filter(email=self.cleaned_data.get('email')).exists():
                raise forms.ValidationError('Email already in use')
        return self.cleaned_data.get('email')
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self) -> str:
        user: User = self.instance
        if self.cleaned_data.get('email') != '':
            if User.objects.filter(email=self.cleaned_data.get('email')).exclude(pk=user.pk).exists():
                raise forms.ValidationError('Email already in use')
        return self.cleaned_data.get('email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')