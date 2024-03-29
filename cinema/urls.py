from django.urls import path, include

from .views import all_users, change_user_data_by_admin, \
                    add_banners, \
                    all_movies, movie_detail, new_movie, del_movie, \
                    new_cinema, all_cinemas, cinema_detail, del_cinema, \
                    cinema_hall_detail, del_cinema_hall, new_cinema_hall

app_name = 'cinema'

urlpatterns = [
    path('all_users/', all_users, name='all_users'),
    path('change_user_data_by_admin/<int:pk>/', change_user_data_by_admin, name='change_user_data_by_admin'),

    path('add_banners/', add_banners, name="banners"),

    path('all_movies/', all_movies, name="all_movies"),
    path('new_movie/', new_movie, name='new_movie'),
    path('movie_detail/<int:pk>/', movie_detail, name='movie_detail'),
    path('del_movie/<int:pk>/', del_movie, name='del_movie'),

    path('movie_detail/new_cinema/', new_cinema, name='new_cinema'),# что за ерунда с названием
    path('all_cinemas/', all_cinemas, name='all_cinemas'),
    path('cinema_detail/<int:pk>/', cinema_detail, name='cinema_detail'),
    path('del_cinema/<int:pk>/', del_cinema, name='del_cinema'),
    
    path('cinema_hall_detail/<int:pk>/', cinema_hall_detail, name='cinema_hall_detail'),
    path('del_cinema_hall/<cinema_id>:<int:pk>/', del_cinema_hall, name='del_cinema_hall'),
    path('new_cinema_hall/<int:cinema_id>/', new_cinema_hall, name='new_cinema_hall'),
]