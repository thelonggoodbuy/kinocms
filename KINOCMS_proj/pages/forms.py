from django import forms
from django.core.files.images import get_image_dimensions
from django.core import validators
from django.forms.utils import ErrorList

from .models import NewsAndPromotions

from cinema.widgets import CustomClearableFileInput
from cinema.models import Galery, SeoBlock



class SimpleTextErrorList(ErrorList):
    def __str__(self):
        return self.as_simple_text()

    def as_simple_text(self):
        if not self:
            return ''
        for x in self:
            text = ''.join(x)
        return text

class GaleryImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png', 'jpeg'), )],
                            error_messages={
                                'invalid_image': 'Этот формат не поддерживается'},
                            widget=CustomClearableFileInput(attrs={'class': 'justify-content-center align-self-center text-center'}))

    class Meta:
        model = Galery
        fields = ('image',)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image != None:
            width, height = get_image_dimensions(image)
            if width != 1000:
                raise forms.ValidationError("Ширина маэ складати 1000 пікселів.")
            if height != 190:
                raise forms.ValidationError("Висота маэ складати 150 пікселів.")
        return image




class NewsForm(forms.ModelForm):
    title_news_or_promo = forms.CharField(label = "Назва новини",
                                    error_messages={'required': 'новина має містити назву'}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    date_news_or_promoptions = forms.DateField(required=True)

    description_news_or_promo = forms.CharField(label = "Текст новини", 
                                    error_messages={'required': 'Новина має містити текст'},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))

    url_to_video = forms.URLField(required=False, label = "посилання на відео",
                                    widget=forms.URLInput(attrs={'class': 'form-control'}))

    date_news_or_promoptions = forms.DateField(required=False, 
                                                label = "дата публікації")

    class Meta:
        model = NewsAndPromotions
        fields = ('title_news_or_promo', 'date_news_or_promoptions', 'description_news_or_promo', 'url_to_video', 'date_news_or_promoptions')


class MainImage(forms.ModelForm):
    image = forms.ImageField(label='Головна картинка', required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
                            error_messages={
                                'invalid_image': 'Этот формат не поддерживается'},
                            widget=CustomClearableFileInput())


    DELETE_IMAGE = forms.BooleanField(
        required=False,
        initial=False,
    )

    def save(self, commit=True):
        if self.cleaned_data['DELETE_IMAGE']:
            return self.instance.delete()
        
        return super(MainImage, self).save()


    class Meta:
        model = Galery
        fields = ('image',)

class GaleryImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png', 'jpeg'), )],
                            error_messages={
                                'invalid_image': 'такий формат не підтримується'},
                            widget=CustomClearableFileInput(attrs={'class': 'justify-content-center align-self-center text-center'}))

    class Meta:
        model = Galery
        fields = ('image',)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image != None:
            width, height = get_image_dimensions(image)
            if width != 1000:
                raise forms.ValidationError("Ширина маэ складати 1000 пікселів.")
            if height != 190:
                raise forms.ValidationError("Висота маэ складати 190 пікселів.")
        return image


class SeoBlockForm(forms.ModelForm):
    url_seo = forms.URLField(label = "URL",
                                    error_messages={'invalid': 'Введіть корректну URL адрессу',
                                                    'required': "це поле обовязков'язкове"}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    title_seo = forms.CharField(label = "Title",
                                    error_messages={'required': "це поле обовязков'язкове"},
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    keyword_seo = forms.CharField(label = "Keywords",
                                    error_messages={'required': "це поле обовязков'язкове"}, 
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))
    description_seo = forms.CharField(label = "Description:",
                                    error_messages={'required': "це поле обовязков'язкове"},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"6"}))
   

    class Meta:
        model = SeoBlock
        fields = ('url_seo', 'title_seo', 'keyword_seo', 'description_seo')
