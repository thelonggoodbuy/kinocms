from django import forms
from django.core.files.images import get_image_dimensions
from django.core import validators
from django.forms.utils import ErrorList
from tempus_dominus.widgets import DatePicker
from KINOCMS_proj.settings import DATE_INPUT_FORMATS

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import NewsAndPromotions, Phones

from cinema.widgets import CustomClearableFileInput
from cinema.models import Galery, SeoBlock
from pages.models import CustomPages, MainPage, ContactCell
from cinema.widgets import CustomClearableFileInputBanner






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
                                    error_messages={'required': 'Поле "Назва" не повинно залишатися пустим'}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    date_news_or_promoptions = forms.DateField(required=True, 
                                                widget=forms.DateInput(format = '%m/%d/%Y', attrs={"type":"text", 
                                                                                "class": "form-control datetimepicker-input", 
                                                                                "data-target": "#datetimepicker4"}), 
                                                input_formats=DATE_INPUT_FORMATS)

    description_news_or_promo = forms.CharField(label = "Опис", 
                                    error_messages={'required': 'Поле "Опис" не повинно залишатися пустим'},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))

    url_to_video = forms.URLField(required=False, label = "посилання на відео",
                                    widget=forms.URLInput(attrs={'class': 'form-control'}))
    

    is_active = forms.CheckboxSelectMultiple()

    class Meta:
        model = NewsAndPromotions
        fields = ('title_news_or_promo', 'date_news_or_promoptions', 'description_news_or_promo', 'url_to_video', 'date_news_or_promoptions', 'is_active')


class CustomPageForm(forms.ModelForm):
    title = forms.CharField(label = "Назва",
                                    error_messages={'required': 'Поле "Назва" не повинно залишатися пустим'}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))


    description = forms.CharField(label = "Опис", 
                                    error_messages={'required': 'Поле "Опис" не повинно залишатися пустим'},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))

    is_active = forms.CheckboxSelectMultiple()

    class Meta:
        model = CustomPages
        fields = ('title', 'description', 'is_active')

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
    url_seo = forms.URLField(label = " Seo URL",
                                    error_messages={'invalid': 'Введіть корректну URL адрессу',
                                                    'required': "це поле обовязков'язкове"}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    title_seo = forms.CharField(label = "Seo Назва",
                                    error_messages={'required': "це поле обовязков'язкове"},
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    keyword_seo = forms.CharField(label = "Seo ключові слова",
                                    error_messages={'required': "це поле обовязков'язкове"}, 
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))
    description_seo = forms.CharField(label = "Seo Опис",
                                    error_messages={'required': "це поле обовязков'язкове"},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"6"}))
   

    class Meta:
        model = SeoBlock
        fields = ('url_seo', 'title_seo', 'keyword_seo', 'description_seo')


class MainPageForm(forms.ModelForm):
    is_active = forms.CheckboxSelectMultiple()
    main_page_seo_text = forms.CharField(label = "SEO текст:",
                                    error_messages={'required': "SEO текст э обовязковим"},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"8"}))
    class Meta:
        model = MainPage
        fields = ('is_active', 'main_page_seo_text')

class PhoneForm(forms.ModelForm):
    number = PhoneNumberField(required=False, label='телефон',
                            error_messages={'invalid': "Введіть номер телефону одного з мобільних операторів України. Введений номер не є коректним."},
                            widget=PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Phones
        fields = ('number',)

class ContactCellForm(forms.ModelForm):

    cinema_name = forms.CharField(label = "Назва кінотеатру",
                                    error_messages={'required': 'Контакт кінотеатру має містити назву'}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    is_active = forms.CheckboxSelectMultiple()
    address = forms.CharField(label = "Адреса кінотеатру",
                                    error_messages={'required': "це поле обовязков'язкове"}, 
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))
    location = forms.CharField(label = "Координати кінотеатру",
                                    error_messages={'required': "це поле обовязков'язкове"}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label='Изображение', required=False, 
                                    validators=[validators.FileExtensionValidator(
                                    allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
                                    error_messages={
                                        'invalid_image': 'Файли з таким розширенням не підтримуються'},
                                    widget=CustomClearableFileInput(attrs={'class': 'justify-content-center align-self-center text-center'}))

    class Meta:
        model = ContactCell
        fields = ('cinema_name', 'is_active', 'address', 'location', 'logo')