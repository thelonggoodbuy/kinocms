from django.urls import path

from .views import all_news, news_detail, create_news, del_news,\
                    all_promo, create_promo, promo_detail, promo_del,\
                    all_pages, create_page, page_detail, page_del,\
                    main_page_detail, contacts_detail,\
                    statistics,\
                    main_page, all_cinemas, about_cinema, front_all_promo, front_promo_detail,\
                    front_schedule, schedule_sort_cinema, schedule_sort_cinema_hall, \
                    front_book_ticket, book_ticket_per_place, \
                    front_playbill
                    
                    

app_name = 'pages'

urlpatterns = [
    path('', main_page, name='main_page'),

    path('all_news/', all_news, name='all_news'),
    path('news_detail/<int:pk>/', news_detail, name='news_detail'),
    path('create_news/', create_news, name='create_news'),
    path('del_news/<int:pk>/', del_news, name='del_news'),

    path('all_promo/', all_promo, name='all_promo'),
    path('create_promo/', create_promo, name='create_promo'),
    path('promo_detail/<int:pk>/', promo_detail, name='promo_detail'),
    path('promo_del/<int:pk>/', promo_del, name='promo_del'),

    path('all_pages/', all_pages, name='all_pages'),
    path('create_page/', create_page, name='create_page'),
    path('page_detail/<int:pk>/', page_detail, name='page_detail'),
    path('page_del/<int:pk>/', page_del, name='page_del'),

    path('main_page_detail/<int:pk>/', main_page_detail, name='main_page_detail'),
    path('contacts_detail/<int:pk>/', contacts_detail, name="contacts_detail"),

    path('statistics/', statistics, name='statistics' ),

    path('all_cinemas/', all_cinemas, name='all_cinemas'),
    path('about_cinema/<int:pk>/', about_cinema, name='about_cinema'),

    path('promo_list/', front_all_promo, name='front_all_promo'),
    path('front_promo_detail/<int:pk>/', front_promo_detail, name='front_promo_detail'),

    path('front_schedule/', front_schedule, name='front_schedule'),
    path('front_schedule/ajax/schedule_sort_cinema/', schedule_sort_cinema, name='schedule_sort_cinema'),
    path('front_schedule/ajax/schedule_sort_cinema_hall/', schedule_sort_cinema_hall, name='schedule_sort_cinema_hall'),

    path('front_book_ticket/<int:show_pk>/', front_book_ticket, name='front_book_ticket'),
    path('front_book_ticket/ajax/book_ticket_per_place', book_ticket_per_place, name='book_ticket_per_place'),

    path('front_playbill/', front_playbill, name='front_playbill'),

]