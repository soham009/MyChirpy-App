from django.contrib import admin
from django.urls import path,re_path,reverse_lazy

from client_leads.views import *

app_name = 'client_leads'

urlpatterns = [
path('client/leads',all_leads_data,name='client/leads'),

path('client/add_leads',create_lead_view,name='client/add_leads'),

# path('otp_varification',otp_submit,name='otp_varification'),

# path('dashboard',dashboard,name='dashboard'),

# path('users',all_users,name='users'),
]    