from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _


from .models import CustomUser

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


    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError({'confirm_password': 'пароли не совпадают'})


    class Meta:
        model = CustomUser
        fields = ("email", "password", "confirm_password")



# class RegisterUserForm(forms.ModelForm):
#     email = forms.EmailField(required=True,
#                             label="Адрес электронной почты",
#                             widget=forms.EmailInput(attrs={'class': 'form-control',
#                                                         'placeholder':'email'}))
#     password1 = forms.CharField(label='Пароль',
#                             widget=forms.PasswordInput(attrs={'class': 'form-control',
#                                                             'placeholder':'password'})                                                            )
#     password2 = forms.CharField(label='Пароль(повторно)',
#                             widget=forms.PasswordInput(attrs={'class': 'form-control',
#                                                             'placeholder':'password'})
#                             )

#     def clean_password1(self):
#         password1 = self.cleaned_data['password1']
#         if password1:
#             password_validation.validate_password(password1)
#         return password1

#     def clean(self):
#         password1 = self.cleaned_data['password1']
#         password2 = self.cleaned_data['password2']
#         if password1 and password2 and password1 != password2:
#             errors ={'password2': ValidationError(
#                 'Введенные пароли не совпадают', code='password_mismatch')}
#             raise ValidationError(errors)

#     def save(self, commit=True):
#         if commit:
#             user.save()
#         user_registered.send(RegisterUserForm, instance=user)
#         return user



#     class Meta:
#         model = CustomUser
#         fields = ("email", "password1", "password2")






# class RegisterUserForm(forms.ModelForm):
#     email = forms.EmailField(required=True,
#                             label="Адрес электронной почты",
#                             widget=forms.EmailInput(attrs={'class': 'form-control',
#                                                         'placeholder':'email'}))
#     password = forms.CharField(label='Пароль',
#                             widget=forms.PasswordInput(attrs={'class': 'form-control',
#                                                             'placeholder':'password'})                                                            )
#     password = forms.CharField(label='Пароль(повторно)',
#                             widget=forms.PasswordInput(attrs={'class': 'form-control',
#                                                             'placeholder':'password'})
#                             )




#     class Meta:
#         model = CustomUser
#         fields = ("email", "password")
