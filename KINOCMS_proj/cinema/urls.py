from django.urls import path, include

from .views import all_users

app_name = 'cinema'

urlpatterns = [
    path('all_users/', all_users, name='all_users')
]