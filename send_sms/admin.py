from django.contrib import admin
from send_sms.models import SMS_Usage
# Register your models here.

class SMSUsageAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "send_to_number",
        "send_from",
        "status",
        "send_date_time",
    ]
admin.site.register(SMS_Usage,SMSUsageAdmin)    