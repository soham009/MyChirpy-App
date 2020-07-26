from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from email_manager.models import EmailMaster
from accounts.models import Portal_User
from email_manager.serializer import EmailSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@api_view(['GET',])
def all_email_view(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_emails = EmailMaster.objects.filter(client_id=user)
        serializer = EmailSerializer(all_emails,many=True)
        return Response(serializer.data)  
    

@api_view(['POST',])
def create_email_view(request):
    email = EmailMaster()
    data = {}
    if request.method == "POST":
        serializer = EmailSerializer(email, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['response']="Email Registered Successfully"
            return Response(data)
        return Response(serializer.errors)

@api_view(['GET',])
def email_detail_view(request,pk):
    try:
        email = EmailMaster.objects.get(pk=pk)
    except EmailMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "GET":
        serializer = EmailSerializer(email)
        return Response(serializer.data)  
    
@api_view(['POST',])
def email_update_view(request,pk):

    try:
        email = EmailMaster.objects.get(pk=pk)
    except EmailMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        serializer = EmailSerializer(email, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response']="Email Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors)    

@api_view(['DELETE',])
def email_delete_view(request,pk):

    try:
        email = EmailMaster.objects.get(pk=pk)
    except EmailMaster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = email.delete()
        data = {}
        if operation:
            data['success']="Delete Successfully"
        else:
            data['failure']="Delete Failed"   
        return Response(data=data)
        
@login_required(login_url = '/accounts/admin_login')
def all_emails(request,pk):
    client_object = Portal_User.objects.get(pk=pk)
    all_data = EmailMaster.objects.filter(client_id=client_object)
    data={'all_data':all_data,'user':client_object}      
    return render(request,'email_manager/email_master.html',data)
