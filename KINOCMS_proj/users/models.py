from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.forms import BooleanField, CharField, EmailField, JSONField

# from cinema.models import Show


class CustomUser(AbstractBaseUser):
    LANGUAGES = (
        ('ua', 'Українська мова'),
        ('ru', 'Русский язык'),
    )
    SEX = (
        ('male', 'Мужской пол'),
        ('female', 'Женский пол'),
    )
    name = CharField(max_length=50)
    surname = CharField(max_length=50)
    nickname = CharField(max_length=50)
    email = EmailField(max_length=50)
    address = CharField(max_length=50)
    card_id = CharField(max_length=20)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='ru')
    sex = models.CharField(max_length=15, choices=SEX)
    phone_number = models.CharField(max_length=20)
    born = models.DateField()
    letters = models.ManyToManyField('Mailing')

    def __str__(self):
        return f"{self.name} {self.surname}"


class Mailing(models.Model):
    letter_name = CharField(max_length=25)
    template = models.FileField()

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