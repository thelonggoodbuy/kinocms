from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList
from django.core.validators import RegexValidator
import re
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import validate_password

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget

from .models import CustomUser, Mailing
from .widgets import CustomTemplateFileInput



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
                            label="email",
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

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError({
                "password":["Password and confirm_password does not match"]
                })

    class Meta:
        model = CustomUser
        fields = ("email", "password", "confirm_password")




class LoginForm(forms.Form):
    email = forms.EmailField(label='email',
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder':'email'}))
    password = forms.CharField(label='Пароль',
                            widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                            'placeholder':'password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        taken_email = CustomUser.objects.filter(email=email)
        if taken_email.exists() is False:
            self.add_error('email', 'пользователь с таким email не зарегистрирован')
        return email


    class Meta:
        model = CustomUser
        fields = ("email", "password")


class ChangeUserForm(forms.ModelForm):

    name = forms.CharField(required=False, label="Имя",
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'name'}))

    surname = forms.CharField(required=False, label="Фамилия",
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'surname'}))

    nickname = forms.CharField(required=False, label="Псевдоним",
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'nickname'}))

    email = forms.EmailField(required=False, label="email",
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                        'placeholder':'email'}))

    address = forms.CharField(required=False, label="Адрес",
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder':'address'}))


    card_id = forms.CharField(required=False, label='Номер банковской карты',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'card_id_number'}))

    language = forms.ChoiceField(required=False, label='Язык',
                            choices=(('ua', 'Українська мова'), ('ru', 'Русский язык')),
                            initial='ru',
                            widget=forms.RadioSelect())

    sex = forms.ChoiceField(required=False, label='Пол',
                            choices=(('male', 'Мужской пол'), ('female', 'Женский пол')),
                            widget=forms.RadioSelect())

    phone_number = PhoneNumberField(required=False, label='Номер телефона',
                            widget=PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control'}))

    town = forms.CharField(required=False, label="Город",
                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder':'town'}))

    password = forms.CharField(required=False, label='Пароль',
                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                    'placeholder':'password'}))
                                            
    confirm_password = forms.CharField(required=False, label='Повторите пароль',
                        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                        'placeholder':'password'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        other_user = CustomUser.objects.get(email=email)
        if other_user and other_user.id != self.instance.id:
            self.data = self.data.copy()
            self.data['email'] = self.instance.email
            raise forms.ValidationError("Один из пользователей системы уже использует такой email")
        return email


    def clean(self):
        cleaned_data = super(ChangeUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if self.cleaned_data['password'] != '':
            password = self.cleaned_data['password']
            validate_password(password)

        if password != confirm_password:
            raise forms.ValidationError({
                "password":["Пароли не совпадают"]
                })

        
    class Meta:
        model = CustomUser
        fields = ("name", "surname", "nickname", "email", "address",
                 "card_id", "language",
                 "sex", "town", "phone_number", "born", "password", "confirm_password")

        widgets = {
            'born': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'})}



class SendBoxForm(forms.ModelForm):

    template = forms.FileField(widget = forms.ClearableFileInput())
    
    class Meta:
        model = Mailing
        fields = ("template", "users")
        widgets = {
            'users': forms.CheckboxSelectMultiple()
        }


    # def get_uploaded_filename(self):
    #     try:
    #         self.data['template']
    #         return self.cleaned_data['template']
    #     except:
    #         pass

class UpdateBoxForm(forms.ModelForm):

    # template = forms.FileField(required=False, widget = forms.FileInput())
    # users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Mailing
        fields = ("users", )
        widgets = {
            'users': forms.CheckboxSelectMultiple()
        }