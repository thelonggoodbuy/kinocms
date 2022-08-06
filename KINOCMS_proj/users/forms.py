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

    phone_number = forms.CharField(required=False, label='Номер телефона',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'phone_number'}))

    town = forms.CharField(required=False, label="Город",
                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder':'town'}))




    def clean_email(self):
        email = self.cleaned_data['email']
        other_user = CustomUser.objects.get(email=email)
        if other_user and other_user.id != self.instance.id:
            self.data = self.data.copy()
            self.data['email'] = self.instance.email
            raise forms.ValidationError("Один из пользователей системы уже использует такой email")
        return email



    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if phone == "":
            self.data = self.data.copy()
            self.data['phone_number'] = ""
        elif bool(re.search(r"^((\+38\d{10}$)|(38\d{10})|(\d{10})|(\d{9}))$", phone)) is False:
            self.data = self.data.copy()
            self.data['phone_number'] = self.instance.phone_number
            self.add_error('phone_number', 'Введите номер телефона одного из телефонных операторов Украины ') 
        else:
            if bool(re.search(r"^\+38\d{10}$", phone)) is True:
                phone=phone
            elif bool(re.search(r"^38\d{10}$", phone)) is True: 
                phone = f"+{phone}"
                print(phone)
            elif bool(re.search(r"^\d{10}$", phone)) is True: 
                phone = f"+38{phone}"
            elif bool(re.search(r"^\d{9}$", phone)) is True: 
                phone = f"+380{phone}"
        return phone

    
    

    class Meta:
        model = CustomUser
        fields = ("name", "surname", "nickname", "email", "address",
                 "card_id", "language",
                 "sex", "town", "phone_number", "born")

        widgets = {
            'born': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'})}


class ChangeUserPassword(forms.ModelForm):

    password = forms.CharField(required=False, label='Пароль',
                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                    'placeholder':'password'}))
                                            
    confirm_password = forms.CharField(required=False, label='Повторите пароль',
                        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                        'placeholder':'password'}))



    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super(ChangeUserPassword, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError({
                "password":["Пароли не совпадают"]
                })

    class Meta:
        model = CustomUser
        fields = ("password", "confirm_password")