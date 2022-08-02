from django import forms



class SearchUserForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')