from genericpath import exists
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import createsuperuser
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Команда ініціалізації користувачів сайту'

    def handle(self, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email='initial_simple_user_1@gmail.com')
            print('\nInitial users is already exist. New initial users haven`t been created.\n')
        except:
            password = '12345asdfg'
            email_1='initial_simple_user_1@gmail.com'
            email_2='initial_simple_user_2@gmail.com'
            email_3='initial_simple_user_3@gmail.com'
            user_1 = CustomUser(email=email_1, is_superuser=False, is_staff=False)
            user_1.set_password(password)
            user_1.save()
            user_2 = CustomUser(email=email_2, is_superuser=False, is_staff=False)
            user_2.set_password(password)
            user_2.save()
            user_3 = CustomUser(email=email_3, is_superuser=False, is_staff=False)
            user_3.set_password(password)
            user_3.save()
            print('\n')
            print('Initial simple users have been created!')
            print('Initial simple users emails are:')
            print('initial_simple_user_1@gmail.com')
            print('initial_simple_user_2@gmail.com')
            print('initial_simple_user_3@gmail.com')
            print('All initial simple users have password is 12345asdfg')
            print('\n')