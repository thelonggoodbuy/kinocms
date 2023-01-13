from django.core.management.base import BaseCommand
import random

from users.models import Ticket, CustomUser
from cinema.models import Show



class Command(BaseCommand):
    help = 'Команда додавання придбанних квитків для статистики'

    all_shows = [show for show in Show.objects.all()]
    users_id_list = [user for user in CustomUser.objects.filter(is_superuser=False)]

    def handle(self, *args, **kwargs):
        for show in self.all_shows:
            current_show_cost = show.cost
            iterations = random.randrange(0, 10)
            for index in range(0, iterations):
                generated_ticket =  Ticket(
                    show=show,
                    user=(random.choices(self.users_id_list))[0],
                    ticket_type=(random.choices(['booking', 'buying']))[0],
                    cost=current_show_cost                    
                )
                generated_ticket.save()