from django import forms
from django.core import validators
from django.forms.utils import ErrorList
from django.core.files.images import get_image_dimensions
# from django.utils import image


from .widgets import CustomClearableFileInput, CustomClearableFileInputBanner
# from .models import Galery, BannerWithTimeScrolling
from .models import Galery, BannerCell, HighestBannerWithTimeScrolling, ThroughBackroundBanner, BannerPromotionsAndNews, Movie, SeoBlock




class SimpleTextErrorList(ErrorList):
    def __str__(self):
        return self.as_simple_text()

    def as_simple_text(self):
        if not self:
            return ''
        for x in self:
            text = ''.join(x)
        return text

class SearchUserForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'label': '',
                                                                'placeholder': 'поиск'}))
    


# Banner forms
TIME_SCROLLING_CHOICE_TIME = (
    ('1', '1'),
    ('3', '3'),
    ('5', '5'),
    ('8', '8'),
    ('10', '10'),
)

class HighestBannerForm(forms.ModelForm):
    on_of_status = forms.CheckboxSelectMultiple()
    timescrolling = forms.ChoiceField(choices=TIME_SCROLLING_CHOICE_TIME)


    class Meta:
        model = HighestBannerWithTimeScrolling
        fields = ('on_of_status', 'timescrolling')




class AddBannerCellForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение', required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
                            error_messages={
                                'invalid_image': 'Файли з таким розширенням не підтримуються'},
                            widget=CustomClearableFileInputBanner())

    url = forms.URLField(required=False, 
                        error_messages={'invalid': 'Введіть корректну URL адрессу'}, 
                        label='URL', 
                        widget=forms.URLInput())
    text = forms.CharField(error_messages={'required': 'Баннер має містити назву або текст'},
                            widget=forms.TextInput())
    purpose = forms.CharField(initial = 'highest_banner')


    def clean_image(self):
        image = self.cleaned_data.get("image")
        width, height = get_image_dimensions(image)
        if width != 1090:
            raise forms.ValidationError("Ширина має складати 1090 пікселів.")
        if height != 150:
            raise forms.ValidationError("Висота має складати 150 пікселів.")
        return image




    class Meta:
        model = BannerCell
        fields = ('url', 'text', 'image', 'purpose')


class ThroughBackroundBannerForm(forms.ModelForm):
    background_type = forms.ChoiceField(required=False,
                                        choices=(('background_photo', 'фото на фоне'), ('simple_photo', 'просто фото')),
                                        initial='simple_photo',
                                        widget=forms.RadioSelect())
    

    class Meta:
        model = ThroughBackroundBanner()
        fields = ('background_type',)


class AddPhotoToGalleryForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение', required=False, 
                        validators=[validators.FileExtensionValidator(
                        allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
                        error_messages={
                                'invalid_image': 'Файли з таким розширенням не підтримуються'},
                        widget=CustomClearableFileInputBanner())
    
    delete_image = forms.BooleanField(
        required=False,
        initial=False,
    )

    def clean_image(self):
        image = self.cleaned_data.get("image")
        width, height = get_image_dimensions(image)
        if width != 2000:
            raise forms.ValidationError("Ширина має складати 2000 пікселів.")
        if height != 3000:
            raise forms.ValidationError("Висота має складати 3000 пікселів.")
        return image


    def save(self, commit=True):
        if self.cleaned_data['delete_image']:
            return self.instance.delete()
        return super(AddPhotoToGalleryForm, self).save()
    

    class Meta:
        model = Galery
        fields = ('image',)



class BannerPromotionsAndNewsForm(forms.ModelForm):
    on_of_status = forms.CheckboxSelectMultiple()
    timescrolling = forms.ChoiceField(choices=TIME_SCROLLING_CHOICE_TIME)


    class Meta:
        model = BannerPromotionsAndNews
        fields = ('on_of_status', 'timescrolling')


class AddBannerPromotionAndNewsCellForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение', required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
                            error_messages={
                            'invalid_image': 'Файли з таким розширенням не підтримуються'},
                            widget=CustomClearableFileInputBanner())

    url = forms.URLField(required=False, 
                        error_messages={'invalid': 'Введіть корректну URL адрессу'}, 
                        label='URL', 
                        widget=forms.URLInput())
    text = forms.CharField(required=False, widget=forms.TextInput())
    purpose = forms.CharField(initial = 'banner_news_and_promotions')

    class Meta:
        model = BannerCell
        fields = ('url', 'text', 'image', 'purpose')




    def clean_image(self):
        image = self.cleaned_data.get("image")
        width, height = get_image_dimensions(image)
        if width != 1000 or height != 190:
            raise forms.ValidationError("Зображення має мати розмір 1000 на 190 пікселів.")
        # if height != 150:
        #     raise forms.ValidationError("Висота має складати 150 пікселів.")
        return image




# Movie Forms
class MovieForm(forms.ModelForm):
    title_movie = forms.CharField(label = "Название фильма",
                                    error_messages={'required': 'Фільма має містити назву'}, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    description_movie = forms.CharField(label = "Описание фильма", 
                                    error_messages={'required': 'Фільма має містити опис'},
                                    widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3"}))
    url_to_trailer = forms.URLField(required=False, label = "ссылка на трейлер",
                                    widget=forms.URLInput(attrs={'class': 'form-control'}))
    type_2d = forms.BooleanField(required=False, label = "2d",
                                    widget=forms.CheckboxInput(attrs={"class": "form-check-input", 
                                                                        "type": "checkbox", 
                                                                        "id": "inlineCheckbox1", 
                                                                        "value": "option1"}))
    type_3d = forms.BooleanField(required=False, label = "3d",
                                    widget=forms.CheckboxInput(attrs={"class": "form-check-input", 
                                                                    "type": "checkbox", 
                                                                    "id": "inlineCheckbox1", 
                                                                    "value": "option1"}))
    type_IMAX = forms.BooleanField(required=False, label = "IMAX",
                                    widget=forms.CheckboxInput(attrs={"class": "form-check-input", 
                                                                        "type": "checkbox", 
                                                                        "id": "inlineCheckbox1", 
                                                                        "value": "option1"}))

    class Meta:
        model = Movie
        fields = ('title_movie', 'description_movie', 'type_2d', 'type_3d', 'type_IMAX', 'url_to_trailer')

    def clean(self):
        type_2d = self.cleaned_data['type_2d']
        type_3d = self.cleaned_data['type_3d']
        type_IMAX = self.cleaned_data['type_IMAX']
        if (type_2d or type_3d or type_IMAX) is False:
            raise forms.ValidationError("Потрібно обрати хоча б один вариант показу")
       


class MovieMainImage(forms.ModelForm):
    image = forms.ImageField(label='Главная картинка', required=False, 
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
        return super(MovieMainImage, self).save()


    class Meta:
        model = Galery
        fields = ('image',)



class MovieGaleryImageForm(forms.ModelForm):
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
        width, height = get_image_dimensions(image)
        if width != 1000:
            raise forms.ValidationError("Ширина маэ складати 1000 пікселів.")
        if height != 190:
            raise forms.ValidationError("Висота маэ складати 150 пікселів.")
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