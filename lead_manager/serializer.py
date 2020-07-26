from rest_framework import serializers
from lead_manager.models import Leads

class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Leads
        fields= ['pk','client_id', 'name', 'company_name', 'designation','address','telephone_no','email_id','mobile_no','website']
