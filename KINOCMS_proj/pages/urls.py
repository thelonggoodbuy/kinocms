from django.urls import path

from .views import index, all_news, news_detail, create_news

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('all_news/', all_news, name='all_news'),
    path('news_detail/<int:pk>/', news_detail, name='news_detail'),
    path('create_news/', create_news, name='create_news'),
]