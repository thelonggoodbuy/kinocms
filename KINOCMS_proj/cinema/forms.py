from django import forms
from django.core import validators


from .widgets import CustomClearableFileInput
# from .models import Galery, BannerWithTimeScrolling
from .models import Galery, BannerCell, HighestBannerWithTimeScrolling


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
                            widget=forms.ClearableFileInput())
                            # widget=forms.ClearableFileInput())

    url = forms.URLField(required=False, widget=forms.URLInput())
    text = forms.CharField(required=False, widget=forms.TextInput())


    class Meta:
        model = BannerCell
        fields = ('url', 'text', 'image')


    # def clean_galery(self):

    #     galery_obj = self.cleaned_data['galery']

    #     try:
    #         goal_object = Galery.objects.get(image=self.instance.galery)
    #     except:
    #         goal_object = Galery(image=galery_obj)

    #     self.data = self.data.copy()
    #     self.data['galery'] = goal_object.id
    #     return galery_obj

        # if goal_object == None:
        #     self.data = self.data.copy()
        #     goal_object.image = self.data['galery']
        #     goal_object = Galery.objects.create()
           
        #     goal_object.image = 



# class AddImageToForm(forms.ModelForm):

#     image = forms.ImageField(label='Изображение', required=False, 
#                         validators=[validators.FileExtensionValidator(
#                         allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
#                         error_messages={
#                             'invalid_extension': 'Этот формат не поддерживается'},
#                         widget=forms.ClearableFileInput())
                        
#     class Meta:
#         model = Galery
#         fields = ('image',)


# class AddImageToGalery(forms.ModelForm):
#     image = forms.ImageField(label='Изображение', required=False, 
#                             validators=[validators.FileExtensionValidator(
#                             allowed_extensions=('gif', 'jpg', 'png', 'jpeg'))],
#                             error_messages={
#                                 'invalid_extension': 'Этот формат не поддерживается'},
#                             # widget=forms.ClearableFileInput())
#                             widget=CustomClearableFileInput())


#     # delete_image = forms.BooleanField(label='удалить', default='False')

#     class Meta:
#         model = Galery
#         fields = ('image',)