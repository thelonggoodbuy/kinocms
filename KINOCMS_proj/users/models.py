from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.forms import BooleanField, CharField, EmailField, JSONField
from django.contrib.auth.models import UserManager
from phonenumber_field.modelfields import PhoneNumberField


# from cinema.models import Show
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    LANGUAGES = (
        ('ua', 'Українська мова'),
        ('ru', 'Русский язык'),
    )
    SEX = (
        ('male', 'Мужской пол'),
        ('female', 'Женский пол'),
    )
    username = None
    password = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    card_id = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='ru')
    sex = models.CharField(max_length=15, choices=SEX)
    phone_number = PhoneNumberField(null=True, blank=True)
    born = models.DateField(null=True, blank=True)
    # letters = models.ManyToManyField('Mailing')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



    def __str__(self):
        return f"{self.id}"


class Mailing(models.Model):
    # letter_name = models.CharField(max_length=25)
    template = models.FileField(upload_to='mailing_templates/')
    users =  models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.letter_name

class MailingStatistic(models.Model):
    many_of_sended_list = models.PositiveIntegerField()

class Ticket(models.Model):
    cancel_show = 'Сеанс отменен, свяжитесь с администрацией кинотеатра'
    STATUS = (
        ('booking', 'бронь'),
        ('buying', 'покупка'),
    )
    show = models.ForeignKey('cinema.Show', on_delete=models.SET(cancel_show))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=20, choices=STATUS)
    plase = models.JSONField()