from django.db import models
from accounts.models import Portal_User
# Create your models here.

class Leads(models.Model):
    client_id = models.ForeignKey(Portal_User,on_delete=models.CASCADE)
    name = models.CharField(max_length=264)
    company_name = models.CharField(max_length=264,blank=True)
    designation= models.CharField(max_length=264,blank=True)
    address = models.TextField(max_length=500,blank=True)
    telephone_no = models.CharField(max_length=264,blank=True)
    email_id = models.EmailField()
    mobile_no = models.CharField(max_length=264)
    website = models.CharField(max_length=264,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    