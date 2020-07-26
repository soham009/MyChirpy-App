from django.contrib import admin
from accounts.models import Portal_User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("pk","user_role","email","username","Mobile_No","Otp")

admin.site.register(Portal_User,UserAdmin)    