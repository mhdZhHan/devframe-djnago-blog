from django import forms
from django.contrib.auth.models import User

from articles.models import Article


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ))

    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}
    ))
    first_name = forms.CharField(label='Full Name', widget=forms.TextInput(
        attrs={'placeholder': 'Full Name'}
    ))

    class Meta:
        model = User
        fields = ('first_name', 'email', 'username')
        widgets = {
            # 'first_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Work Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_confirm_password(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('Passord dont match. ')
        return data['confirm_password']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body')


class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body')
