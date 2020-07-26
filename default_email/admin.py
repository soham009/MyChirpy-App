from django.contrib import admin
from default_email.models import Default_Email
# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "subject",
        "message",
    ]

admin.site.register(Default_Email,EmailAdmin)