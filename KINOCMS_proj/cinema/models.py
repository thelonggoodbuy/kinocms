from django.db import models
from django.forms import ImageField, URLField



class Cinema(models.Model):
    title_cinema = models.CharField(max_length=30)
    description_cinema = models.TextField()
    conditions_cinema = models.TextField()
    logo = models.OneToOneField('Galery', on_delete=models.PROTECT)
    image_top_banner = models.OneToOneField('Galery',related_name='cinema_image_top_banner', on_delete=models.PROTECT)
    image_galery = models.ManyToManyField('Galery', related_name='cinema_image_galery')
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.PROTECT)

    def __str__(self):
        return self.title_cinema


class CinemaHall(models.Model):
    number_cinema_hall = models.SmallIntegerField()
    description_cinema_hall = models.TextField()
    schema_hall = models.ImageField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    image_top_banner = models.OneToOneField('Galery', on_delete=models.PROTECT)
    image_galery = models.ManyToManyField('Galery', related_name='cinemahall_image_galery')
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.cinema}. Зал №{self.number_cinema_hall}"


class Show(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    date_show = models.DateField()
    time_show = models.TimeField()
    total_booked = models.JSONField()
    total_bought = models.JSONField()


class ShowCost(models.Model):
    Show = models.ForeignKey(Show, on_delete=models.CASCADE)
    cost = models.PositiveSmallIntegerField()


class Movie(models.Model):
    title_movie = models.CharField(max_length=150)
    description_movie = models.TextField()
    main_image = models.OneToOneField('Galery', on_delete=models.PROTECT)
    image_galery = models.ManyToManyField('Galery', related_name='movie_image_galery')
    url_to_trailer = models.URLField()
    cinema = models.ManyToManyField(Cinema)
    type_2d = models.BooleanField(default=True)
    type_3d = models.BooleanField(default=False)
    type_IMAX = models.BooleanField(default=False)
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.CASCADE)
    movie_distribution_start = models.DateField(null=True, blank=True)
    movie_distribution_finish = models.DateField(null=True, blank=True)
    release_year = models.PositiveSmallIntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    music_by = models.CharField(max_length=50, null=True, blank=True)
    producer = models.CharField(max_length=50, null=True, blank=True)
    director = models.CharField(max_length=50, null=True, blank=True)
    operator = models.CharField(max_length=50, null=True, blank=True)
    screen_by = models.CharField(max_length=50, null=True, blank=True)
    genre = models.CharField(max_length=20, null=True, blank=True)
    budget = models.CharField(max_length=20, null=True, blank=True)
    age_rating = models.CharField(max_length=20, null=True, blank=True)
    runing_time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title_movie


class Galery(models.Model):
    image = models.ImageField(verbose_name='Изображения',
                        upload_to='galery/')
    special_goal = models.CharField(max_length=50, blank=True, null=True)

# !!!!!!!!!!!!!!
class HighestBannerWithTimeScrolling(models.Model):
    on_of_status = models.BooleanField(default=True)
    timescrolling = models.SmallIntegerField(null=True, blank=True)
    # banner_cell = models.ManyToManyField("BannerCell", null=True, blank=True)


class ThroughBackroundBanner(models.Model):
    BACKGROUND = (
        ('background_photo', 'фото на фоне'),
        ('simple_photo', 'просто фото'),
    )
    background_type = models.CharField(max_length=30, choices=BACKGROUND, default='simple_photo')
    background = models.OneToOneField('Galery', on_delete=models.CASCADE, null=True, blank=True)
    

class BannerCell(models.Model):
    # galery = models.OneToOneField(Galery, on_delete=models.CASCADE, null=True)
    image = models.ImageField(verbose_name='Изображения', upload_to='galery/')
    url = models.URLField(null=True)
    text = models.CharField(null=True, max_length=350)


class SeoBlock(models.Model):
    url_seo = models.URLField()
    title_seo = models.CharField(max_length=200)
    keyword_seo = models.TextField()
    description_seo = models.TextField()