from django.urls import path, include

from .views import all_users, change_user_data_by_admin, add_banners, all_movies, movie_detail, new_movie, all_cinemas, cinema_detail

app_name = 'cinema'

urlpatterns = [
    path('all_users/', all_users, name='all_users'),
    path('change_user_data_by_admin/<int:pk>/', change_user_data_by_admin, name='change_user_data_by_admin'),
    path('add_banners/', add_banners, name="banners"),
    path('all_movies/', all_movies, name="all_movies"),
    path('movie_detail/<int:pk>/', movie_detail, name='movie_detail'),
    # path('movie_detail/new_movie/', new_movie, name='new_movie'),
    path('all_cinemas/', all_cinemas, name='all_cinemas'),
    path('cinema_detail/<int:pk>/', cinema_detail, name='cinema_detail'),
]