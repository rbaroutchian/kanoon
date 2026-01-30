from django import forms
from . models import user
from django.core.exceptions import ValidationError
from django.core import validators


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = user
        fields = ['first_name', 'last_name','email','mobile', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند')

        return cleaned_data

class LoginModelForm(forms.Form):
    username = forms.CharField(label='شماره موبایل')
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='رمز عبور'
    )


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['first_name', 'last_name', 'mobile','address']
