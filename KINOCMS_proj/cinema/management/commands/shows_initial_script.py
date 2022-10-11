from cinema.models import Show


class Command(BaseCommand):
    help = 'Створення шоу на найближчий тиждень'

    def handle(self, *args, **kwargs):
        pass