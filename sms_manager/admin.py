from django.contrib import admin
from sms_manager.models import SMSMaster
# Register your models here.
class SMSMasterAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "client_id",
        "subject",
        "message",
    ]
admin.site.register(SMSMaster,SMSMasterAdmin)    