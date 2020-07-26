from django.contrib import admin
from default_sms.models import Default_SMS
# Register your models here.
class SMSAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "subject",
        "message",
    ]
admin.site.register(Default_SMS,SMSAdmin)    