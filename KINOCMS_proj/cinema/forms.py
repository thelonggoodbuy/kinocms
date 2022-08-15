from django import forms
from django.core import validators


from .widgets import CustomClearableFileInput
from .models import Galery, BannerWithTimeScrolling


class SearchUserForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'label': '',
                                                                'placeholder': 'поиск'}))
    


class AddImageToGalery(forms.ModelForm):
    image = forms.ImageField(label='Изображение', required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png'))],
                            error_messages={
                                'invalid_extension': 'Этот формат не поддерживается'},
                            # widget=forms.ClearableFileInput())
                            widget=CustomClearableFileInput(attrs={'class': 'color: red'}))


    # delete_image = forms.BooleanField(label='удалить', default='False')

    class Meta:
        model = Galery
        fields = ('image',)


