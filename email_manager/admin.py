from django.contrib import admin
from email_manager.models import EmailMaster
# Register your models here.
class EmailMasterAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "client_id",
        "subject",
        "message",
    ]

admin.site.register(EmailMaster,EmailMasterAdmin)