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

    # password = forms.CharField(required=False, label='Пароль',
    #                         widget=forms.PasswordInput(attrs={'class': 'form-control',
    #                                                         'placeholder':'password'})                                                            )

    card_id = forms.CharField(required=False, label='Номер банковской карты',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'card_id_number'}))

    language = forms.CharField(label='Язык',required=False)

    sex = forms.CharField(label='Пол', required=False)

    phone_number = forms.CharField(required=False, label='Номер телефона',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'phone_number'}))

    # confirm_password = forms.CharField(required=False, label='Пароль(повторно)',
    #                         widget=forms.PasswordInput(attrs={'class': 'form-control',
    #                                                         'placeholder':'confirm password'}))

   

 
    def clean_email(self):
        email = self.cleaned_data['email']
        compare_obj = CustomUser.objects.get(email=email)
        if self.instance.pk != compare_obj.pk:
            self.data = self.data.copy()
            self.data['email'] = self.instance.email
            self.add_error('email', f'email {compare_obj.email} занят')

        return email


    class Meta:
        model = CustomUser
        # fields = ("name", "surname", "nickname", "email", "address",
        #          "password", "card_id", "language",
        #          "sex", "phone_number", "confirm_password")
        fields = ("name", "surname", "nickname", "email", "address",
            "card_id", "language",
            "sex", "phone_number")
