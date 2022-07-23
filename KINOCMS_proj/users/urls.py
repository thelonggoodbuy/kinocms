from django.urls import path
from users.views import login, sign_up



app_name='users'

urlpatterns = [
    # path('users/login/', login, name='login'),
    path('sign_up/', sign_up, name='sign_up'),
]
