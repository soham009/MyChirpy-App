from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from send_sms.views import *


app_name = 'send_sms'

urlpatterns = [
path('bulk_sms_data/<int:pk>',bulk_sms_data,name='bulk_sms_data'),

path('send_bulk_sms/<int:pk>',send_bulk_sms,name='send_bulk_sms'),

path('all_send_sms/<int:pk>',all_send_sms_leads,name='all_send_sms'),

path('update_lead_status/<int:pk>',update_lead_status,name='update_lead_status'),

path('send_sms_master/<int:pk>',all_send_sms_to_lead,name='send_sms_master'),

]    