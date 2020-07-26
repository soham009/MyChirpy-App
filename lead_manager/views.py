from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from lead_manager.models import Leads
from accounts.models import Portal_User
from lead_manager.serializer import LeadSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@api_view(['GET',])
def all_leads_view(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_leads = Leads.objects.filter(client_id=user)
        serializer = LeadSerializer(all_leads,many=True)
        return Response(serializer.data)  
    

@api_view(['POST',])
def create_lead_view(request):
    lead = Leads()
    data = {}
    if request.method == "POST":
        serializer = LeadSerializer(lead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['response']="Lead Registered Successfully"
            return Response(data)
        return Response(serializer.errors)

@api_view(['GET',])
def lead_detail_view(request,pk):
    try:
        lead = Leads.objects.get(pk=pk)
    except Leads.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "GET":
        serializer = LeadSerializer(lead)
        return Response(serializer.data)  
    
@api_view(['POST',])
def lead_update_view(request,pk):

    try:
        lead = Leads.objects.get(pk=pk)
    except Leads.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        serializer = LeadSerializer(lead, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response']="Lead Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors)    

@api_view(['DELETE',])
def lead_delete_view(request,pk):

    try:
        lead = Leads.objects.get(pk=pk)
    except Leads.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = lead.delete()
        data = {}
        if operation:
            data['success']="Delete Successfully"
        else:
            data['failure']="Delete Failed"   
        return Response(data=data)
        
@login_required(login_url = '/accounts/admin_login')        
def all_leads(request,pk):
    client_object = Portal_User.objects.get(pk=pk)
    all_data = Leads.objects.filter(client_id=client_object)
    data={'all_data':all_data,'user':client_object}      
    return render(request,'lead_manager/card_master.html',data)
    