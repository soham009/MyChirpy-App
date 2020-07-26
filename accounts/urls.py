from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from accounts.views import *


app_name = 'accounts'

urlpatterns = [
path('register',registration_view,name='register'),

path('login',CustomAuthToken.as_view(),name='login'),

path('user_login',user_login,name='user_login'),

path('otp_varification',otp_submit,name='otp_varification'),

path('dashboard',dashboard,name='dashboard'),

path('users',all_users,name='users'),

path('delete_user/<int:pk>',delete_user,name='delete_user'),

path('update_user/<int:pk>',update_user,name='update_user'),

path('admin_login',admin_login,name='admin_login'),

path('admin_logout',admin_logout,name='admin_logout'),

path('clients',clients,name='clients'),

path('client_dashboard/<int:pk>',client_dashboard,name='client_dashboard'),
]