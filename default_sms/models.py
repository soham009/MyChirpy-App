from django.db import models

# Create your models here.
class Default_SMS(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)