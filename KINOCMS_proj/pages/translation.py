from modeltranslation.translator import translator, TranslationOptions, register
from .models import NewsAndPromotions, CustomPages, ContactCell, MainPage, Contact



@register(NewsAndPromotions)
class NewsAndPromotionsTranslationOptions(TranslationOptions):
    fields = ('title_news_or_promo', 'description_news_or_promo')

@register(CustomPages)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@register(ContactCell)
class CinemaHallTranslationOptions(TranslationOptions):
    fields = ('cinema_name', 'address')



@register(MainPage)
class CinemaHallTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Contact)
class ContactTranslations(TranslationOptions):
    fields = ('title',)