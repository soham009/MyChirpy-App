from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from default_email.views import *


app_name = 'default_email'

urlpatterns = [

    path('all_default_email',all_default_email,name='all_default_email'),

    path('send_default_emails/<int:pk>',send_bulk_email,name='send_default_emails'),

    path('default_emails',default_email,name='default_emails'),

    path('update_email/<int:pk>',update_email,name='update_email'),

    path('delete_email/<int:pk>',delete_email,name='delete_email'),
]