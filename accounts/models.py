from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class Portal_User(AbstractUser):
    ADMIN = 1
    CLIENT = 2
    ROLE_CHOICES = (
      (ADMIN,'Admin'),
      (CLIENT,'Client'))
    user_role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default=ADMIN)
    Mobile_No = models.CharField(max_length=264,blank=True)
    Otp = models.CharField(max_length=264,blank=True)
    Varified = models.BooleanField(default=False)
    update_on = models.DateTimeField(auto_now=True)  
    account_type = models.BooleanField(default=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)    