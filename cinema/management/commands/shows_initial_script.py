from cinema.models import Show, CinemaHall, Movie
from django.core.management.base import BaseCommand
from django.utils.datetime_safe import datetime, time
from datetime import timedelta
import random




class Command(BaseCommand):
    help = 'Створення показів на найближчий тиждень'
    
    test_shows = Show.objects.all()
    if test_shows.exists():
        print('\nCMS have shows. Shows initialization is aborted. \n')
    else: 

        shows_dates = [] 
        for day_of_show in range(1, 7):
            date = datetime.now().date() + timedelta(days=day_of_show)
            shows_dates.append(date)
            
        shows_time = []
        for seanse_time in range(1, 18, 3):
            seanse = datetime.combine(datetime.now(),time(8, 0)) + timedelta(hours=seanse_time)
            shows_time.append(seanse.time())

        all_movies = Movie.objects.all()

        all_cinema_halls = CinemaHall.objects.all()

        def handle(self, *args, **kwargs):
            for show_date in self.shows_dates:
                for show_time in self.shows_time:
                    Show.objects.get_or_create(
                        movie = (random.choice(self.all_movies)),
                        cinema_hall = (random.choice(self.all_cinema_halls)),
                        date_show = show_date,
                        time_show = show_time,
                        cost = 100
                    )
        print('\nInit shows have created.\n')