from genericpath import exists
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import createsuperuser
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Команда ініціалізації адміністратора сайту'

    def handle(self, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email='initial_superuser@gmail.com')
            print('\nInitial superuser is already exist. New initial superuser hasn`t been created.\n')
        except:
            password = '12345asdfg'
            email='initial_superuser@gmail.com'
            user = CustomUser(email=email, is_superuser=True, is_staff=True)
            user.set_password(password)
            user.save()
            print('\n')
            print('Initial superuser has been created!')
            print('Initial superuser email is initial_superuser@gmail.com')
            print('Initial superuser password is 12345asdfg')
            print('\n')