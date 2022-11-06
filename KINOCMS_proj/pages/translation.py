from modeltranslation.translator import translator, TranslationOptions, register
from .models import NewsAndPromotions, CustomPages, ContactCell



@register(NewsAndPromotions)
class NewsAndPromotionsTranslationOptions(TranslationOptions):
    fields = ('title_news_or_promo', 'description_news_or_promo')

@register(CustomPages)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('title_cinema', 'description_cinema', 'conditions_cinema')

@register(ContactCell)
class CinemaHallTranslationOptions(TranslationOptions):
    fields = ('cinema_name', 'address')