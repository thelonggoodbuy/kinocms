from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList


from .models import CustomUser



class SimpleTextErrorList(ErrorList):
    def __str__(self):
        return self.as_simple_text()

    def as_simple_text(self):
        if not self:
            return ''
        for x in self:
            text = ''.join(x)
        return text



class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                            label="Адрес электронной почты",
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                        'placeholder':'email'}))
    password = forms.CharField(label='Пароль',
                            widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                            'placeholder':'password'})                                                            )
    confirm_password = forms.CharField(label='Пароль(повторно)',
                            widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                            'placeholder':'confirm password'}))


    def clean_email(self):
        new_email = self.cleaned_data['email']
        taken_email = CustomUser.objects.filter(email=new_email)
        if taken_email.exists():
            self.add_error('email', 'email занят')
        return new_email


    def clean_confirm_password(self):
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password != confirm_password:
                self.add_error('confirm_password', 'пароли не совпадают')



    class Meta:
        model = CustomUser
        fields = ("email", "password", "confirm_password")




class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль',
                            widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                            'placeholder':'password'}))

    class Meta:
        model = CustomUser
        fields = ("email", "password")