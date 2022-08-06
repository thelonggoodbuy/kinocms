from django.urls import path, include

from .views import all_users, change_user_data_by_admin

app_name = 'cinema'

urlpatterns = [
    path('all_users/', all_users, name='all_users'),
    path('change_user_data_by_admin/<int:pk>/', change_user_data_by_admin, name='change_user_data_by_admin'),
]