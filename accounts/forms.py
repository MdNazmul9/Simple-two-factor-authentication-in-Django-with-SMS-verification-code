from django.forms import ModelForm
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, PasswordInput


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'user_name', 'created_by', 'contact_no', )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].help_text = None
        self.fields['user_name'].help_text = None
        self.fields['password1'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password (again)'})
