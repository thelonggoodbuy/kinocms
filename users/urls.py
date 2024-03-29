from django.urls import path
from users.views import sign_in, sign_up, log_out, change_user_data, del_user, \
                        mailing, del_mailing



app_name='users'

urlpatterns = [
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_up/', sign_up, name='sign_up'),
    path('change_user_data/', change_user_data, name='change_user_data'),
    path('del_user/<int:pk>/', del_user, name='del_user'),
    path('log_out/', log_out, name='log_out'),

    path('mailing/', mailing, name='mailing'),
    path('del_mailing/<int:pk>/', del_mailing, name='del_mailing'),
]
