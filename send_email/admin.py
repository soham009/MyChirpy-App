from django.contrib import admin
from send_email.models import Email_Usage
# Register your models here.

class EmailUsageAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "lead_email",
        "send_from",
        "status",
        "send_date_time",
    ]
admin.site.register(Email_Usage,EmailUsageAdmin)    