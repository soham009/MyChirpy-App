from rest_framework import serializers
from send_email.models import Email_Usage

class Email_UsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email_Usage
        fields= ['pk','send_from', 'lead_name', 'lead_email','status','lead_status','send_date_time']
        
