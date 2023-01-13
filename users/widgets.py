from django import forms


class CustomTemplateFileInput(forms.ClearableFileInput):
    template_name = 'users/widgets_templates/template_input_template.html'