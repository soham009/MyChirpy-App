from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from client_accounts.views import *


app_name = 'client_accounts'

urlpatterns = [
path('client/signup',client_signup,name='client/signup'),

path('client/login',client_login,name='client/login'),

path('client/validation',client_validation,name='client/validation'),

# path('dashboard',dashboard,name='dashboard'),

# path('users',all_users,name='users'),
]    