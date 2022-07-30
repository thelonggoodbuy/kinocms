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
    email = forms.EmailField(label='email',
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder':'email'}))
    password = forms.CharField(label='Пароль',
                            widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                            'placeholder':'password'}))

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

    email = forms.EmailField(required=False, label="Адрес электронной почты",
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

    password = forms.CharField(required=False, label='Пароль',
                        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                        'placeholder':'password'}))
                                            
    confirm_password = forms.CharField(required=False, label='Повторите пароль',
                        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                        'placeholder':'password'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        compare_obj = CustomUser.objects.get(email=email)
        if self.instance.pk != compare_obj.pk:
            self.data = self.data.copy()
            self.data['email'] = self.instance.email
            self.add_error('email', f'email {compare_obj.email} занят')
        return email


 

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            self.add_error('confirm_password', 'пароли не совпадают')

# !

    # def clean_password(self, commifrom django.contrib.auth import update_session_auth_hasht=True):
    #     password = self.cleaned_data['password']
    #     if password == '':
    #         print('Password is empty!')
            
    #         self.data = self.data.copy()
    #         del self.data['password']
    #         del self.data['confirm_password']
    #         print(self.data)
    #         return self.data

    #     return password



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


    # def save(self, commit=True):
    #     user = super(ChangeUserForm, self).save(commit=False)
    #     password = self.cleaned_data["password"]
        # print(len(password))
        # if len(password) == 0:
        #     del self.cleaned_data['password']
        #     del self.cleaned_data['confirm_password']
        #     print(self.cleaned_data)
        #     user.save()
        # else:
        # if len(password) > 0:
        # if commit:
        #     user.set_password(self.cleaned_data["password"])
        # user.save()
        # return user
  


    class Meta:
        model = CustomUser
        fields = ("name", "surname", "nickname", "email", "address",
                 "card_id", "language",
                 "sex", "town", "phone_number", "born")

        widgets = {
            'born': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'})}
