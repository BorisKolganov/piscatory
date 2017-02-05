# coding=utf-8
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from core.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']

    password = forms.CharField(min_length=8, required=True)
    confirm_password = forms.CharField(min_length=8, required=True)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        confirm_password = self.cleaned_data.pop('confirm_password') if 'confirm_password' in self.cleaned_data else None
        if self.cleaned_data.get('password') != confirm_password:
            self._errors['password'] = [u'Пароли не совпадают']
            raise ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        return User.objects.create_user(**self.cleaned_data)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError(
                    u"Пользователь не существует",
                    code='invalid_login',
                    params={'email': "E-mail"},
                )
            if user.is_active:
                self.cleaned_data['user'] = user
        return self.cleaned_data
