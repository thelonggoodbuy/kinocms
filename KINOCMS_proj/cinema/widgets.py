from django import forms


class CustomClearableFileInput(forms.widgets.ClearableFileInput):
    template_name = 'cinema/widgets_templates/customclearablefileinput.html'
