from django.urls import path
from users.views import sign_in, sign_up, log_out



app_name='users'

urlpatterns = [
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_up/', sign_up, name='sign_up'),
    path('', log_out, name='log_out'),
]
