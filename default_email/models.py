from django.db import models
# Create your models here.

class Default_Email(models.Model):
    subject = models.CharField(max_length=1000)
    to = models.CharField(max_length=1000,blank=True)
    greeting = models.CharField(max_length=1000,blank=True)
    message = models.TextField(max_length=2000)
    thank_you = models.CharField(max_length=1000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
