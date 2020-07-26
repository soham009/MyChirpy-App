from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from lead_manager.models import Leads
from default_sms.models import Default_SMS

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import Portal_User
from send_sms.models import SMS_Usage
from send_sms.serializer import SMSUsageSerializer
from default_sms.serializer import Default_SMSSerializer
from lead_manager.serializer import LeadSerializer
import urllib.parse
from accounts.send_sms import replaceSpaces
import urllib.request
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@api_view(['GET',])
def all_default_sms(request):
    if request.method == "GET":
        all_sms = Default_SMS.objects.all()
        serializer = Default_SMSSerializer(all_sms,many=True)
        return Response(serializer.data)  

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
        sms_object = Default_SMS.objects.get(pk=sms_pk)
        message = sms_object.message
        for lead in leads_list:
            lead_object = Leads.objects.get(pk=lead)   
            resp = sendSMS('VmGUZET+Z0g-tG1019iVxThFZtQs8Iqu1JxAnIxMwv', lead_object.mobile_no,'TXTLCL', message)
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

@login_required(login_url = '/accounts/admin_login')
def default_sms(request):
    all_sms = Default_SMS.objects.all()
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        Default_SMS.objects.create(subject=subject,message=message)
        return HttpResponseRedirect(reverse('default_sms:default_sms_data'))
    data = {'all_data':all_sms}
    return render(request,'default_sms/default_sms.html',data)

def update_sms(request,pk):
    sms_object = Default_SMS.objects.get(pk=pk)
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        sms_object.subject = subject
        sms_object.message = message
        sms_object.save()
        return HttpResponseRedirect(reverse('default_sms:default_sms_data'))

def delete_sms(request,pk):
    sms_object = Default_SMS.objects.get(pk=pk)
    sms_object.delete()
    return HttpResponseRedirect(reverse('default_sms:default_sms_data'))
