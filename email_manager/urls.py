from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from email_manager.views import *


app_name = 'email_manager'

urlpatterns = [
path('all_email_view/<int:pk>',all_email_view,name='all_email_view'),

    path('email_create',create_email_view,name='email_create'),

    path('email_detail/<int:pk>',email_detail_view,name='email_detail'),

    path('email_update/<int:pk>',email_update_view,name='email_update'),

    path('email_delete/<int:pk>',email_delete_view,name='email_delete'),

    path('email_data/<int:pk>',all_emails,name='email_data'),
]    