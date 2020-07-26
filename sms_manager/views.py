from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from sms_manager.models import SMSMaster
from accounts.models import Portal_User
from sms_manager.serializer import SMSSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@api_view(['GET',])
def all_sms_view(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_sms = SMSMaster.objects.filter(client_id=user)
        serializer = SMSSerializer(all_sms,many=True)
        return Response(serializer.data)  
    

@api_view(['POST',])
def create_sms_view(request):
    sms = SMSMaster()
    data = {}
    if request.method == "POST":
        serializer = SMSSerializer(sms, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['response']="sms Registered Successfully"
            return Response(data)
        return Response(serializer.errors)

@api_view(['GET',])
def sms_detail_view(request,pk):
    try:
        sms = SMSMaster.objects.get(pk=pk)
    except SMSMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "GET":
        serializer = SMSSerializer(sms)
        return Response(serializer.data)  
    
@api_view(['POST',])
def sms_update_view(request,pk):

    try:
        sms = SMSMaster.objects.get(pk=pk)
    except SMSMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        serializer = SMSSerializer(sms, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response']="Sms Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors)    

@api_view(['DELETE',])
def sms_delete_view(request,pk):

    try:
        sms = SMSMaster.objects.get(pk=pk)
    except SMSMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = sms.delete()
        data = {}
        if operation:
            data['success']="Delete Successfully"
        else:
            data['failure']="Delete Failed"   
        return Response(data=data)

@login_required(login_url = '/accounts/admin_login')
def all_sms(request,pk):
    client_object = Portal_User.objects.get(pk=pk)
    all_data = SMSMaster.objects.filter(client_id=client_object)
    data={'all_data':all_data,'user':client_object}      
    return render(request,'sms_manager/sms_master.html',data)
