from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from lead_manager.views import *


app_name = 'lead_manager'

urlpatterns = [

    path('all_leads_view/<int:pk>',all_leads_view,name='all_leads_view'),

    path('lead_create',create_lead_view,name='lead_create'),

    path('lead_detail/<int:pk>',lead_detail_view,name='lead_detail'),

    path('lead_update/<int:pk>',lead_update_view,name='lead_update'),

    path('lead_delete/<int:pk>',lead_delete_view,name='lead_delete'),

    path('leads_data/<int:pk>',all_leads,name='leads_data'),
    
]    