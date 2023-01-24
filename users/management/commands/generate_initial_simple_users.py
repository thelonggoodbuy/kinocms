from genericpath import exists
from django.core.management.base import BaseCommand
from django.contrib.auth.management.commands import createsuperuser
from users.models import CustomUser
import random

from faker import Faker
fake = Faker('uk_UA')

class Command(BaseCommand):
    help = 'Команда ініціалізації користувачів сайту'
    cities = ['Київ', 'Житомир', 'Одесса',\
             'Чернівці', 'Вінниця', 'Чернігів',\
            'Львів', 'Івано-Франківськ', 'Черкаси']

    def handle(self, *args, **kwargs):
        test_users_query = CustomUser.objects.all()
        if test_users_query.exists():
            print('\nSome users are already created. New users hasn`t been created.\n')
        else:
            for index in range(1, 15):   
                password = '12345asdfg'
                if CustomUser.objects.filter(email=f'initial_simple_user_{index}@gmail.com'):
                    continue
                else:
                    email=f'initial_simple_user_{index}@gmail.com'
                    fake_name=fake.name()
                    fake_list=fake_name.split(' ')
                    surname = fake_list[-1]
                    name = fake_list[-2]
                    user=CustomUser(email=email,
                                    is_active=True,
                                    is_staff=False,
                                    is_superuser=False,
                                    name=name,
                                    surname=surname,
                                    nickname=fake_name,
                                    town=(random.choices(self.cities))[0],
                                    sex=random.choices(['male', 'female'])[0]
                    )
                    user.set_password(password)
                    user.save()
