from django.db import models
from accounts.models import Portal_User

# Create your models here.
class SMSMaster(models.Model):
    client_id = models.ForeignKey(Portal_User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)