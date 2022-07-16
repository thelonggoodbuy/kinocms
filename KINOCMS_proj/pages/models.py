from django.db import models
from django.forms import CharField, URLField


class CustomPage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_undeleteble = models.BooleanField(default=False)
    main_image = models.OneToOneField('cinema.Galery', related_name='custom_page_main_image', on_delete=models.PROTECT)
    image_galery = models.ManyToManyField('cinema.Galery')
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT)


class Contact(models.Model):
    cinema = models.OneToOneField('cinema.Cinema', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    address = models.TextField()
    location = models.CharField(max_length=50)
    logo = models.OneToOneField('cinema.Galery', on_delete=models.PROTECT)
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT)


class MainPage(models.Model):
    main_page_seo_text = models.TextField()
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

class Phones(models.Model):
    page = models.ForeignKey(MainPage, on_delete=models.CASCADE)
    phone_number = CharField(max_length=30)


class NewsAndPromotions(models.Model):
    type = (
        ('news', 'Новость'),
        ('promotion', 'Акция')
    )
    title_news_or_promo = models.CharField(max_length=30)
    description_news_or_promo = models.TextField()
    date_news_or_promoptions = models.DateField()
    is_active = models.BooleanField(default=True)
    main_image = models.OneToOneField('cinema.Galery', on_delete=models.PROTECT)
    image_galery = models.ManyToManyField('cinema.Galery', related_name='news_and_promotions_galery')
    type = models.CharField(max_length=30 ,choices=type)
    url_to_video = URLField()
    seo_clock = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT)
