from django.db import models
from accounts.models import Portal_User
# Create your models here.

class EmailMaster(models.Model):
    client_id = models.ForeignKey(Portal_User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=1000)
    to = models.CharField(max_length=1000,blank=True)
    greeting = models.CharField(max_length=1000,blank=True)
    message = models.TextField(max_length=2000)
    thank_you = models.CharField(max_length=1000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
