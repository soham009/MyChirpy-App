from rest_framework import serializers
from sms_manager.models import SMSMaster

class SMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMSMaster
        fields= ['pk','client_id', 'subject','message']
