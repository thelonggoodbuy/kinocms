from modeltranslation.translator import translator, TranslationOptions, register
from .models import Movie, Cinema, CinemaHall



@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title_movie', 'description_movie')

@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('title_cinema', 'description_cinema', 'conditions_cinema')

@register(CinemaHall)
class CinemaHallTranslationOptions(TranslationOptions):
    fields = ('cinema_hall_name', 'description_cinema_hall')

