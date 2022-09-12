from django import forms


class CustomClearableFileInput(forms.widgets.ClearableFileInput):
    template_name = 'cinema/widgets_templates/customclearablefileinput.html'

class CustomClearableFileInputBanner(forms.widgets.ClearableFileInput):
    template_name = 'cinema/widgets_templates/customclearablefileinputbanner.html'

class CustomTextAreaWithEditor(forms.widgets.Textarea):
    template_name = 'cinema/widgets_templates/custom_text_area_with_editor.html'