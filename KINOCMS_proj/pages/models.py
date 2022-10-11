from django.db import models
from django.forms import CharField, URLField


class CustomPages(models.Model):
    issue_variable = (
        ('about_cinema', 'про кінотеатр'),
        ('cafe_bar', 'кафе-бар'),
        ('vip-hall', 'VIP-зала'),
        ('advertising', 'реклама'),
        ('childrens_room', 'дитяча кімната'),


    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_undeleteble = models.BooleanField(default=False)
    main_image = models.OneToOneField('cinema.Galery', related_name='custom_page_main_image', on_delete=models.PROTECT, null=True)
    image_galery = models.ManyToManyField('cinema.Galery', null=True)
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT, null=True)
    special_issue = models.CharField(max_length=100, choices=issue_variable, null=True, blank=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    cinema = models.OneToOneField('cinema.Cinema', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    address = models.TextField()
    location = models.CharField(max_length=50)
    logo = models.OneToOneField('cinema.Galery', on_delete=models.PROTECT)
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT)


class MainPage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    date_created = models.DateField(auto_now_add=True, blank=True)
    main_page_seo_text = models.TextField()
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Phones(models.Model):
    page = models.ForeignKey(MainPage, on_delete=models.CASCADE)
    number = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.number


class NewsAndPromotions(models.Model):
    type_variable = (
        ('news', 'Новость'),
        ('promotion', 'Акция')
    )

    title_news_or_promo = models.CharField(max_length=300)
    description_news_or_promo = models.TextField()
    date_news_or_promoptions = models.DateField()
    is_active = models.BooleanField(default=True)
    main_image = models.OneToOneField('cinema.Galery', on_delete=models.PROTECT)
    image_galery = models.ManyToManyField('cinema.Galery', related_name='news_and_promotions_galery')
    publ_type = models.CharField(max_length=30, choices=type_variable, blank=True)
    url_to_video = models.URLField(null=True, blank=True)
    seo_block = models.OneToOneField('cinema.SeoBlock', on_delete=models.PROTECT)

    def __str__(self):
        return self.title_news_or_promo