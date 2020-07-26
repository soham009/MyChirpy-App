from django.contrib import admin
from lead_manager.models import Leads
# Register your models here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ("pk","client_id","name","email_id","mobile_no")

admin.site.register(Leads,LeadAdmin)    