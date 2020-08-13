from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.api.views import (
    registration_view,
    user_login
)
app_name = 'users'
urlpatterns = [
    path('registration/',registration_view,name='user_registration'),
    path('login/',user_login,name='login')
]