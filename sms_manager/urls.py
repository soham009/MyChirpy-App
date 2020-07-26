from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from sms_manager.views import *


app_name = 'sms_manager'

urlpatterns = [
path('all_sms_view/<int:pk>',all_sms_view,name='all_sms_view'),

    path('sms_create',create_sms_view,name='sms_create'),

    path('sms_detail/<int:pk>',sms_detail_view,name='sms_detail'),

    path('sms_update/<int:pk>',sms_update_view,name='sms_update'),

    path('sms_delete/<int:pk>',sms_delete_view,name='sms_delete'),

    path('sms_data/<int:pk>',all_sms,name='sms_data'),
]    