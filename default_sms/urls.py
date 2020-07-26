from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from default_sms.views import *


app_name = 'default_sms'

urlpatterns = [

     path('all_default_sms',all_default_sms,name='all_default_sms'),

    path('send_default_sms/<int:pk>',send_bulk_sms,name='send_default_sms'),

    path('default_sms_data',default_sms,name='default_sms_data'),

    path('update_sms/<int:pk>',update_sms,name='update_sms'),

    path('delete_sms/<int:pk>',delete_sms,name='delete_sms'),

]