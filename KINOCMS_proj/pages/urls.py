from django.urls import path

from .views import index, all_news, news_detail

app_name = 'pages'

urlpatterns = [
    path('', index, name='index'),
    path('all_news/', all_news, name='all_news'),
    path('news_detail/<int:pk>/', news_detail, name='news_detail'),
]