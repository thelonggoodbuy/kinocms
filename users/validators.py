import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                ugettext("Пароль должен содержать хотя бы 1 цифру."),
                code='password_no_number'
            )

    def get_help_text(self):
        return ugettext(
            "Пароль должен содержать хотя бы 1 цифру."
        )

class UpercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                ugettext("Пароль должен содержать хотя бы 1 большую букву."),
                code='password_no_upper_case'
            )

    def get_help_text(self):
        return ugettext(
            "Пароль должен содержать хотя бы 1 большую букву."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                ugettext("Пароль должен содержать хотя бы 1 маленькую букву."),
                code='password_no_lower_case'
            )

    def get_help_text(self):
        return ugettext(
            "Пароль должен содержать хотя бы 1 маленькую букву."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                ugettext("Пароль должен содержать хотя бы 1 специальный знак."),
                code='password_no_symbol'
            )

    def get_help_text(self):
        return ugettext(
            "Пароль должен содержать хотя бы 1 специальный знак."
        )