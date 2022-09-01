from django import forms
from django.core import validators


from .widgets import CustomClearableFileInput
# from .models import Galery, BannerWithTimeScrolling
from .models import Galery, BannerCell, HighestBannerWithTimeScrolling, ThroughBackroundBanner


class SearchUserForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'label': '',
                                                                'placeholder': 'поиск'}))
    

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
    banner_cell = forms.CheckboxSelectMultiple()

    class Meta:
        model = HighestBannerWithTimeScrolling
        fields = ('on_of_status', 'timescrolling', 'banner_cell')




class AddBannerCellForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение', required=False, 
                            validators=[validators.FileExtensionValidator(
                            allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
                            error_messages={
                                'invalid_extension': 'Этот формат не поддерживается'},
                            widget=CustomClearableFileInput())


    url = forms.URLField(required=False, 
                        label='URL', 
                        widget=forms.URLInput())
    text = forms.CharField(required=False, widget=forms.TextInput())


    class Meta:
        model = BannerCell
        fields = ('url', 'text', 'image')


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
                            'invalid_extension': 'Этот формат не поддерживается'},
                        widget=CustomClearableFileInput())

    def clean(self):
        image = self.data['image']
        print(f'this is self data: {image}')
        if self.data['image'] == '':
            print('this object must be empty!')
            # delete_image = Galery.objects.get(id=self.instance.pk)
            # self.instance.delete()
            print(self.instance)



    class Meta:
        model = Galery
        fields = ('image',)