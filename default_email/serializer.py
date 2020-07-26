from rest_framework import serializers
from default_email.models import Default_Email

class Default_EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Default_Email
        fields= ['pk', 'subject', 'to', 'greeting','message','thank_you']
