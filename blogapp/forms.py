# forms.py
from django import forms
from .models import post, comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title', 'author', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['comment_author', 'content']


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2