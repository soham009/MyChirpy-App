from rest_framework import serializers
from email_manager.models import EmailMaster

class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailMaster
        fields= ['pk','client_id', 'subject', 'to', 'greeting','message','thank_you']
