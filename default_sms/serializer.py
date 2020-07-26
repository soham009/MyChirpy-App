from rest_framework import serializers
from default_sms.models import Default_SMS

class Default_SMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = Default_SMS
        fields= ['pk','subject','message']
