from rest_framework import serializers
from send_sms.models import SMS_Usage

class SMSUsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMS_Usage
        fields= ['pk','send_from', 'send_to_name', 'send_to_number', 'send_message','status','lead_status','send_date_time']
        
