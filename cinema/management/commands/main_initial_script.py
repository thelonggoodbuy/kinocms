from genericpath import exists
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
import datetime

from django.core.files import File

from users.models import CustomUser

from pages.models import CustomPages, MainPage, NewsAndPromotions

from cinema.models import HighestBannerWithTimeScrolling, ThroughBackroundBanner, BannerPromotionsAndNews,\
                             BannerCell, Galery, Cinema, SeoBlock, CinemaHall,\
                             Movie


from faker import Faker


from django.conf import settings
import os
base_dir = settings.BASE_DIR
fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Команда ініціалізації користувачів сайту'

    def handle(self, *args, **kwargs):
        path_to_sample_media = str(base_dir) + '/cinema/management/sample_data/sample_media'
        path_to_sample_texts = str(base_dir) + '/cinema/management/sample_data/sample_text'

    # ---------------highest banners----------------------

        highest_banner_with_time_scrolling = HighestBannerWithTimeScrolling(pk=1, on_of_status=True, timescrolling=10)
        highest_banner_with_time_scrolling.save()

        test_banners_query = BannerCell.objects.filter(purpose='highest_banner')
        if test_banners_query.exists():
            print('\nCMS have or more highest_banners. current initialization is broked. \n')
        else:
            higest_banner_image_1 = BannerCell(
                url="http://test_url_1.net",
                text="верхній баннер 1",
                purpose='highest_banner',
                image=UploadedFile(
                    file=open((path_to_sample_media + '/hight_banner/hight_banner1.png'), 'rb')
                )
            )
            higest_banner_image_1.save()

            higest_banner_image_2 = BannerCell(
                url="http://test_url_2.net",
                text="верхній баннер 2",
                purpose='highest_banner',
                image=UploadedFile(
                    file=open((path_to_sample_media + '/hight_banner/hight_banner2.png'), 'rb')
                )
            )
            higest_banner_image_2.save()
            print('Highest banner with two banner cells have been created.\n')

        # ---------------through_background_banner----------------------
        try:
            test_through_background_banner_query = ThroughBackroundBanner.objects.first()
            print('\n CMS has one or more through_background_banner with an image. current initialization is broked. \n')
        except:

            through_image = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/through_background_banner/through_background_banner.jpg'), 'rb')))
            through_image.save()

            through_background_banner = ThroughBackroundBanner(
                background_type='background_photo',
                background = through_image
            )
            through_background_banner.save()
            print('Through_background_banner has been created.\n')

        # ---------------banner_promotion_and_news----------------------
        banner_promotion_and_news = BannerPromotionsAndNews(pk=1, on_of_status=True, timescrolling=10)
        banner_promotion_and_news.save()

        test_banners_query = BannerCell.objects.filter(purpose='banner_news_and_promotions')
        if test_banners_query.exists():
            print('\nCMS have one or more banner_news_and_promotions. current initialization is broked. \n')
        else:
            news_and_promo_banners_1 = BannerCell(
                url="http://test_url_3.net",
                text="новини та акції",
                purpose='banner_news_and_promotions',
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo_banners/news_and_promo_banners_1.png'), 'rb')
                )
            )
            news_and_promo_banners_1.save()

            news_and_promo_banners_2 = BannerCell(
                url="http://test_url_4.net",
                text="новини та акції",
                purpose='banner_news_and_promotions',
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo_banners/news_and_promo_banners_2.png'), 'rb')
                )
            )
            news_and_promo_banners_2.save()
            print('Banner promotion and news with two banner cells have been created.\n')


        # ---------------add_initial_cinema----------------------
        
        try:
            test_cinema = Cinema.objects.get(title_cinema='Жовтень_Тестовий')
            print('\nCMS have initial cinema in DB. cinema initialization is aborted. \n')
        except:


            with open((path_to_sample_texts + '/cinema/cinema_desciption.txt'), 'r') as f:
                description_text = f.readlines()

            with open((path_to_sample_texts + '/cinema/cinema_conditions.txt'), 'r') as f:
                conditions_text = f.readlines()

            logo = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema/logo.svg'), 'rb')
                )
            )
            logo.save()

            image_top_banner = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema/Hight_banner.png'), 'rb')
                )
            )
            image_top_banner.save()

            galery_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema/galery_image_1.png'), 'rb')
                )
            )
            galery_image_1.save()

            galery_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema/galery_image_2.png'), 'rb')
                )
            )
            galery_image_2.save()

            seo_cinema = SeoBlock(
                url_seo='http://test_url_1_cinema.net',
                title_seo='initial cinema seo title',
                keyword_seo='keywords for cinema',
                description_seo='initital description seo'
            )
            seo_cinema.save()


            initial_cinema = Cinema(
                title_cinema='Жовтень_Тестовий',
                description_cinema=description_text[0],
                conditions_cinema=conditions_text[0],
                logo=logo,
                image_top_banner=image_top_banner,
                seo_block=seo_cinema,
                on_of_status=True
                )

            initial_cinema.save()
            initial_cinema.image_galery.add(galery_image_1.id)
            initial_cinema.image_galery.add(galery_image_2.id)
            initial_cinema.save()

            # ---------------add_initial_cinema-halls----------------------



            with open((path_to_sample_texts + '/cinema_hall/description_1.txt'), 'r') as f:
                cinema_hall_description_1 = f.readlines()
                

            image_top_banner_cinema_hall_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema_hall/logo_1.jpg'), 'rb')
                )
            )
            image_top_banner_cinema_hall_1.save()


            galery_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema_hall/cinema_hall_galery_1.png'), 'rb')
                )
            )
            galery_image_1.save()

            seo_cinema_hall = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial cinema_hall_1 seo title',
                keyword_seo='keywords for cinema',
                description_seo='initital description seo'
            )
            seo_cinema_hall.save()


            initial_cinema_hall = CinemaHall(
                cinema_hall_name='Зал 1',
                description_cinema_hall=cinema_hall_description_1[0],
                cinema = initial_cinema,
                schema_hall = {"A": 12, "B": 12, "C": 12, "D": 8, "E": 8, "F": 4, "H": 4, "I": 4, "J": 4},
                image_top_banner = image_top_banner_cinema_hall_1,
                seo_block = seo_cinema_hall
            )

            initial_cinema_hall.save()
            initial_cinema_hall.image_galery.add(galery_image_1.id)
            initial_cinema_hall.save()


            with open((path_to_sample_texts + '/cinema_hall/description_2.txt'), 'r') as f:
                cinema_hall_description_2 = f.readlines()

            image_top_banner_cinema_hall_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema_hall/logo_2.jpg'), 'rb')
                )
            )
            image_top_banner_cinema_hall_2.save()


            galery_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/cinema_hall/cinema_hall_galery_2.png'), 'rb')
                )
            )
            galery_image_2.save()

            seo_cinema_hall = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial cinema_hall_2 seo title',
                keyword_seo='keywords for cinema',
                description_seo='initital description seo'
            )
            seo_cinema_hall.save()


            initial_cinema_hall_2 = CinemaHall(
                cinema_hall_name='Зал 2',
                description_cinema_hall=cinema_hall_description_2[0],
                cinema = initial_cinema,
                schema_hall = {"A": 12, "B": 12, "C": 12, "D": 8, "E": 8, "F": 4, "H": 4, "I": 4, "J": 4},
                image_top_banner = image_top_banner_cinema_hall_2,
                seo_block = seo_cinema_hall
            )

            initial_cinema_hall_2.save()
            initial_cinema_hall_2.image_galery.add(galery_image_2.id)
            initial_cinema_hall_2.save()


            # ---------------add_initial_movie_1----------------------

            with open((path_to_sample_texts + '/movie/movie_1.txt'), 'r') as f:
                movie_description_1 = f.readlines()


            main_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_main_image_1.jpg'), 'rb')
                )
            )
            main_image_1.save()

            galery_cinema_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_galery_1_1.jpg'), 'rb')
                )
            )
            galery_cinema_image_1.save()

            galery_cinema_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_galery_1_2.jpg'), 'rb')
                )
            )
            galery_cinema_image_2.save()


            seo_cinema_1 = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial cinema 1 seo title',
                keyword_seo='keywords for cinema',
                description_seo='initital description seo'
            )
            seo_cinema_1.save()


            initial_movie_1 = Movie(
                title_movie='Запрошення',
                description_movie=movie_description_1[0],
                main_image=main_image_1,
                # image_galery
                url_to_trailer='<iframe width="560" height="315" src="https://www.youtube.com/embed/cRniyysaR68" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
                type_2d=True,
                type_3d=False,
                type_IMAX=False,
                seo_block = seo_cinema_1,

                movie_distribution_start = (datetime.date.today() - datetime.timedelta(days=7)),
                movie_distribution_finish = (datetime.date.today() + datetime.timedelta(days=21)),

                release_year=2022,
                country='USA',
                music_by=fake.name(),
                producer=fake.name(),
                director=fake.name(),
                operator=fake.name(),
                screen_by=fake.name(),
                genre='комедія',
                budget='46.4 міліона',
                age_rating='G',
            )

            initial_movie_1.save()
            initial_movie_1.cinema.add(initial_cinema.id)
            initial_movie_1.image_galery.add(galery_cinema_image_1.id)
            initial_movie_1.image_galery.add(galery_cinema_image_2.id)
            initial_movie_1.save()



            # ---------------add_initial_movie_2----------------------

            with open((path_to_sample_texts + '/movie/movie_2.txt'), 'r') as f:
                movie_description_2 = f.readlines()


            main_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_main_image_2.jpeg'), 'rb')
                )
            )
            main_image_2.save()

            galery_cinema_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_galery_2_1.jpg'), 'rb')
                )
            )
            galery_cinema_image_1.save()

            galery_cinema_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_galery_2_2.jpg'), 'rb')
                )
            )
            galery_cinema_image_2.save()


            seo_cinema_1 = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial cinema 2 seo title',
                keyword_seo='keywords for cinema',
                description_seo='initital description seo'
            )
            seo_cinema_1.save()


            initial_movie_2 = Movie(
                title_movie='Електросестри',
                description_movie=movie_description_2[0],
                main_image=main_image_2,
                url_to_trailer='<iframe width="560" height="315" src="https://www.youtube.com/embed/qhGxZyFvEUY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
                type_2d=True,
                type_3d=False,
                type_IMAX=True,
                seo_block = seo_cinema_1,

                movie_distribution_start = (datetime.date.today() - datetime.timedelta(days=7)),
                movie_distribution_finish = (datetime.date.today() + datetime.timedelta(days=21)),

                release_year=2020,
                country='USA',
                music_by=fake.name(),
                producer=fake.name(),
                director=fake.name(),
                operator=fake.name(),
                screen_by=fake.name(),
                genre='документальний',
                budget='5.24 міліона',
                age_rating='G',
            )

            initial_movie_2.save()
            initial_movie_2.cinema.add(initial_cinema.id)
            initial_movie_2.image_galery.add(galery_cinema_image_1.id)
            initial_movie_2.image_galery.add(galery_cinema_image_2.id)
            initial_movie_2.save()


            # ---------------add_initial_movie_3----------------------

            with open((path_to_sample_texts + '/movie/movie_3.txt'), 'r') as f:
                movie_description_3 = f.readlines()


            main_image_3 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_main_image_3.jpeg'), 'rb')
                )
            )
            main_image_3.save()

            galery_cinema_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_galery_3_1.jpg'), 'rb')
                )
            )
            galery_cinema_image_1.save()

            galery_cinema_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/movie/movie_galery_3_2.jpg'), 'rb')
                )
            )
            galery_cinema_image_2.save()


            seo_cinema_3 = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial cinema 3 seo title',
                keyword_seo='keywords for cinema',
                description_seo='initital description seo'
            )
            seo_cinema_3.save()


            initial_movie_3 = Movie(
                title_movie='Квиток до раю',
                description_movie=movie_description_3[0],
                main_image=main_image_3,
                url_to_trailer='<iframe width="560" height="315" src="https://www.youtube.com/embed/jRM2Jk3zo1g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
                type_2d=True,
                type_3d=False,
                type_IMAX=True,
                seo_block = seo_cinema_3,

                movie_distribution_start = (datetime.date.today() + datetime.timedelta(days=7)),
                movie_distribution_finish = (datetime.date.today() + datetime.timedelta(days=21)),

                release_year=2022,
                country='USA',
                music_by=fake.name(),
                producer=fake.name(),
                director=fake.name(),
                operator=fake.name(),
                screen_by=fake.name(),
                genre='триллер',
                budget='5.24 міліона',
                age_rating='G',
            )

            initial_movie_3.save()
            initial_movie_3.cinema.add(initial_cinema.id)
            initial_movie_3.image_galery.add(galery_cinema_image_1.id)
            initial_movie_3.image_galery.add(galery_cinema_image_2.id)
            initial_movie_3.save()

        print('Initial cinema, halls and movies were created!\n')
        #---------------------------------------------------- 
        # ---------------news_and_promo----------------------
        #----------------------------------------------------

        test_news = NewsAndPromotions.objects.filter(publ_type='news')
        if test_news.exists():
            print('\nCMS have news. news initialization is aborted. \n')
        else:
            with open((path_to_sample_texts + '/pages/news.txt'), 'r') as f:
                news_description = f.readlines()

            main_image_news = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo/news.png'), 'rb')
                )
            )
            main_image_news.save()

            galery_news_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo/news_1_galery.jpeg'), 'rb')
                )
            )
            galery_news_image_1.save()

            galery_news_image_2 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo/news_2_galery.jpeg'), 'rb')
                )
            )
            galery_news_image_2.save()


            seo_news = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial news seo title',
                keyword_seo='keywords for news',
                description_seo='initital description seo'
            )
            seo_news.save()


            initial_news = NewsAndPromotions(
                title_news_or_promo='Оголошено номінантів на 5-ту Національну премію кінокритиків «Кіноколо»',
                description_news_or_promo=news_description[0],
                date_news_or_promoptions=(datetime.date.today() + datetime.timedelta(days=2)),
                is_active=True,
                main_image=main_image_news,
                publ_type='news',
                url_to_video='https://youtu.be/TTHF2Dfw1Dg',
                seo_block=seo_news

            )

            initial_news.save()
            initial_news.image_galery.add(galery_news_image_1.id)
            initial_news.image_galery.add(galery_news_image_2.id)
            initial_news.save()
            print('\ninitial news was created. \n')


        test_promo = NewsAndPromotions.objects.filter(publ_type='promotion')
        if test_promo.exists():
            print('\nCMS have promo. promo initialization is aborted. \n')
        else:
            with open((path_to_sample_texts + '/pages/promo.txt'), 'r') as f:
                promo_description = f.readlines()

            main_image_promo = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo/promo.jpeg'), 'rb')
                )
            )
            main_image_promo.save()

            galery_promo_image_1 = Galery(
                image=UploadedFile(
                    file=open((path_to_sample_media + '/news_and_promo/promo_1_galery.jpg'), 'rb')
                )
            )
            galery_promo_image_1.save()


            seo_promo = SeoBlock(
                url_seo='https://www.google.com',
                title_seo='initial promo seo title',
                keyword_seo='keywords for promo',
                description_seo='initital description seo'
            )
            seo_promo.save()


            initial_promo = NewsAndPromotions(
                title_news_or_promo='Фірмова кав’ярня від Multiplex',
                description_news_or_promo=promo_description[0],
                date_news_or_promoptions=(datetime.date.today() + datetime.timedelta(days=2)),
                is_active=True,
                main_image=main_image_promo,
                publ_type='promotion',
                url_to_video='https://youtu.be/TTHF2Dfw1Dg',
                seo_block=seo_promo

            )

            initial_promo.save()
            initial_promo.image_galery.add(galery_promo_image_1.id)
            initial_promo.save()
            print('\ninitial promo was created. \n')



        # ---------------PAGES----------------------

        with open((path_to_sample_texts + '/pages/about_cinema_description.txt'), 'r') as f:
            about_cinema_page_descriptions = f.readlines()

        with open((path_to_sample_texts + '/pages/cafe_bar.txt'), 'r') as f:
            cafe_cinema_page_descriptions = f.readlines()

        with open((path_to_sample_texts + '/pages/vip_hall.txt'), 'r') as f:
            vip_hall_page_descriptions = f.readlines()

        with open((path_to_sample_texts + '/pages/advertising.txt'), 'r') as f:
            advertising_page_descriptions = f.readlines()

        with open((path_to_sample_texts + '/pages/childrens_room.txt'), 'r') as f:
            children_room_page_descriptions = f.readlines()


        try:
            test_custom_page = CustomPages.objects.get(special_issue='about_cinema')
            print('\n CMS about cinema page. current initialization is broked. \n')
        except:
            about_cinema_page = CustomPages(
                title='Про кінотеатр',
                description = about_cinema_page_descriptions[0],
                date_created = datetime.date.today(),
                is_active=True,
                is_undeleteble=True,
                special_issue='about_cinema'
            )
            about_cinema_page.save()
            print('\nAbout cinema page was cerated\n')


        try:
            test_cafe_bar = CustomPages.objects.get(special_issue='cafe_bar')
            print('\n CMS about cafe_bar page. Current initialization is broked. \n')
        except:
            cafe_bar_page = CustomPages(
                title='Кафе бар',
                description = cafe_cinema_page_descriptions[0],
                date_created = datetime.date.today(),
                is_active=True,
                is_undeleteble=True,
                special_issue='cafe_bar'
            )
            cafe_bar_page.save()
            print('\nAbout cafe_bar page was cerated\n')


        try:
            test_vip_hall = CustomPages.objects.get(special_issue='vip-hall')
            print('\n CMS about vip_hall page. Current initialization is broked. \n')
        except:
            VIP_hall_page = CustomPages(
                title='VIP зала',
                description = vip_hall_page_descriptions[0],
                date_created = datetime.date.today(),
                is_active=True,
                is_undeleteble=True,
                special_issue='vip-hall'
            )
            VIP_hall_page.save()
            print('\nAbout vip_hall page was cerated\n')


        try:
            test_advertising = CustomPages.objects.get(special_issue='advertising')
            print('\n CMS about advertising page. Current initialization is broked. \n')
        except:
            advertising_page = CustomPages(
                title='Реклама',
                description = advertising_page_descriptions[0],
                date_created = datetime.date.today(),
                is_active=True,
                is_undeleteble=True,
                special_issue='advertising'
            )
            advertising_page.save()
            print('\nAdvertising page was cerated\n')
        

        try:
            test_advertising = CustomPages.objects.get(special_issue='childrens_room')
            print('\n CMS about childrens_room page. Current initialization is broked. \n')
        except:
            childrens_room_page = CustomPages(
                title='Дитяча кімната',
                description = children_room_page_descriptions[0],
                date_created = datetime.date.today(),
                is_active=True,
                is_undeleteble=True,
                special_issue='childrens_room'
            )
            childrens_room_page.save()
            print('\nChildrens_room page was cerated\n')


        try:
            test_main_page = MainPage.objects.get(main_page_seo_text='Головна сторінка сайту.')
            print('\n CMS about main_page page. Current initialization is broked. \n')
        except:
            main_page = MainPage(
                title='Головна сторінка',
                main_page_seo_text='Головна сторінка сайту.',
                is_active=True,
            )
            main_page.save()
            print('\nMain_page page was cerated\n')

