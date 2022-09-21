from django.urls import path

from .views import index, all_news, news_detail, create_news, del_news,\
                        all_promo, create_promo, promo_detail, promo_del,\
                        all_pages, create_page, page_detail, page_del,\
                        main_page_detail

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),

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
]