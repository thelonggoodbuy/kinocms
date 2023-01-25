from django.db import models
from django.forms import ImageField, URLField
import os
from django.urls import reverse



class Cinema(models.Model):
    title_cinema = models.CharField(max_length=30)
    description_cinema = models.TextField()
    conditions_cinema = models.TextField(null=True)
    logo = models.OneToOneField('Galery', on_delete=models.PROTECT, null=True)
    image_top_banner = models.OneToOneField('Galery',related_name='cinema_image_top_banner', on_delete=models.PROTECT, null=True)
    image_galery = models.ManyToManyField('Galery', related_name='cinema_image_galery')
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.PROTECT, null=True)
    on_of_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title_cinema


class CinemaHall(models.Model):
    cinema_hall_name = models.CharField(max_length=30)
    created_data = models.DateField(auto_now_add=True)
    description_cinema_hall = models.TextField()
    schema_hall = models.JSONField(null=True, blank=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    image_top_banner = models.OneToOneField('Galery', on_delete=models.PROTECT, null=True)
    image_galery = models.ManyToManyField('Galery', related_name='cinemahall_image_galery')
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.cinema_hall_name}"


class Show(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    date_show = models.DateField()
    time_show = models.TimeField()
    total_booked = models.SmallIntegerField(null=True, blank=True)
    total_bought = models.SmallIntegerField(null=True, blank=True)
    cost = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse("pages:front_book_ticket", kwargs={"show_pk": self.pk})

    def __str__(self):
        return f"Сеанс {self.movie}. {self.cinema_hall}. Дата {self.date_show}. Час {self.time_show}."

# class ShowCost(models.Model):
#     Show = models.ForeignKey(Show, on_delete=models.CASCADE)
#     cost = models.PositiveSmallIntegerField()


class Movie(models.Model):
    title_movie = models.CharField(max_length=150)
    description_movie = models.TextField()
    main_image = models.OneToOneField('Galery', on_delete=models.SET_NULL, null=True, blank=True)
    image_galery = models.ManyToManyField('Galery', related_name='movie_image_galery')
    url_to_trailer = models.URLField(max_length=2000)
    cinema = models.ManyToManyField(Cinema)
    type_2d = models.BooleanField(default=True)
    type_3d = models.BooleanField(default=False)
    type_IMAX = models.BooleanField(default=False)
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.PROTECT)
    movie_distribution_start = models.DateField(null=True, blank=True)
    movie_distribution_finish = models.DateField(null=True, blank=True)
    release_year = models.PositiveSmallIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    music_by = models.CharField(max_length=100, null=True, blank=True)
    producer = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    operator = models.CharField(max_length=100, null=True, blank=True)
    screen_by = models.CharField(max_length=100, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    budget = models.CharField(max_length=100, null=True, blank=True)
    age_rating = models.CharField(max_length=100, null=True, blank=True)
    runing_time = models.CharField(max_length=100, null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse("movie", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title_movie


class Galery(models.Model):
    image = models.ImageField(blank=True, verbose_name='Изображения',
                        upload_to='galery/')
    special_goal = models.CharField(max_length=50, blank=True, null=True)



class HighestBannerWithTimeScrolling(models.Model):
    on_of_status = models.BooleanField(default=True)
    timescrolling = models.SmallIntegerField(null=True, blank=True)


class ThroughBackroundBanner(models.Model):
    BACKGROUND = (
        ('background_photo', 'фото на фоне'),
        ('simple_photo', 'просто фото'),
    )
    background_type = models.CharField(max_length=30, choices=BACKGROUND, default='simple_photo')
    background = models.OneToOneField('Galery', on_delete=models.CASCADE, null=True, blank=True)


class BannerPromotionsAndNews(models.Model):
    on_of_status = models.BooleanField(default=True)
    timescrolling = models.SmallIntegerField(null=True, blank=True)
    

class BannerCell(models.Model):

    PURPOSE = (
        ('highest_banner', 'баннер на верхней части страницы'),
        ('banner_news_and_promotions', 'баннер про новости и акции'),
    )
    image = models.ImageField(verbose_name='Изображения', upload_to='galery/')
    url = models.URLField(null=True)
    text = models.CharField(null=True, max_length=350)
    purpose = models.CharField(max_length=50, choices=PURPOSE)


class SeoBlock(models.Model):
    url_seo = models.URLField()
    title_seo = models.CharField(max_length=200)
    keyword_seo = models.TextField()
    description_seo = models.TextField()