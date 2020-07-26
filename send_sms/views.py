from django.shortcuts import render
from lead_manager.models import Leads
from sms_manager.models import SMSMaster

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import Portal_User
from send_sms.models import SMS_Usage
from send_sms.serializer import SMSUsageSerializer
from sms_manager.serializer import SMSSerializer
from lead_manager.serializer import LeadSerializer
import urllib.parse
from accounts.send_sms import replaceSpaces
import urllib.request
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@api_view(['GET',])
def bulk_sms_data(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = {}
        all_leads = Leads.objects.filter(client_id=user)
        all_sms = SMSMaster.objects.filter(client_id=user)
        serializer1 = LeadSerializer(all_leads,many=True)
        serializer2 = SMSSerializer(all_sms,many=True)
        data['leads']= serializer1.data
        data['sms']= serializer2.data
        return Response(data)

@api_view(['POST',])
def send_bulk_sms(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        data = {}
        sms_pk = request.POST['sms_pk']
        leads_list = request.POST.getlist('select_lead')
        sms_object = SMSMaster.objects.get(pk=sms_pk)
        message = sms_object.message
        for lead in leads_list:
            lead_object = Leads.objects.get(pk=lead)   
            resp = sendSMS('', lead_object.mobile_no,'TXTLCL', message)
            dic = json.loads(resp)
            SMS_Usage.objects.create(send_to_name = lead_object.name,
                                send_to_number=lead_object.mobile_no,
                                send_from=user,
                                send_message=message,
                                status= dic['status'])
        data['response']="Sms Send Successfully"
        return Response(data)   

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

@api_view(['GET',])
def all_send_sms_leads(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_send_sms = SMS_Usage.objects.filter(send_from=user)
        serializer = SMSUsageSerializer(all_send_sms,many=True)
        return Response(serializer.data)

@api_view(['POST',])
def update_lead_status(request,pk):
    try:
        send_sms = SMS_Usage.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        data = {}
        lead_status = request.POST['lead_status']
        send_sms.lead_status = lead_status
        send_sms.save()
        data['response']="Status Updated Successfully"
        return Response(data)
        
@login_required(login_url = '/accounts/admin_login')
def all_send_sms_to_lead(request,pk):
    user = Portal_User.objects.get(pk=pk)
    all_data = SMS_Usage.objects.filter(send_from=user)
    data = {'all_data':all_data,'user':user}
    return render(request,'send_sms/send_sms_master.html',data)
