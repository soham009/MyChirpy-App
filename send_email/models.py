from django.db import models
from accounts.models import Portal_User
# Create your models here.
class Email_Usage(models.Model):
    #Total Fields : 5
    #------SMS Usage Table Fields------

    #This field store number to which sms is send
    lead_name = models.CharField(max_length=1000,blank=True)
    lead_email = models.CharField(max_length=1000,blank=True)
    #This field store sms send from which sender ID
    send_from = models.ForeignKey(Portal_User,on_delete=models.CASCADE)
    #This field store status of sms sent
    status = models.CharField(max_length=1000,blank=True)
    lead_status = models.CharField(max_length=1000,blank=True)
    #This field store sms send date time 
    send_date_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.pk)

