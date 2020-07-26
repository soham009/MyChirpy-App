from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from send_email.views import *


app_name = 'send_email'

urlpatterns = [
path('bulk_email_data/<int:pk>',bulk_email_data,name='bulk_email_data'),

path('send_bulk_email/<int:pk>',send_bulk_email,name='send_bulk_email'),

path('all_send_email/<int:pk>',all_send_email_leads,name='all_send_email'),

path('update_lead_status/<int:pk>',update_lead_status,name='update_lead_status'),

path('send_email_master/<int:pk>',all_send_email_to_lead,name='send_email_master'),

]