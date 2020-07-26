from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from email_manager.models import EmailMaster
from accounts.models import Portal_User
from email_manager.serializer import EmailSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def all_emails_data(request):
    user = request.user
    all_emails = EmailMaster.objects.filter(client_id=user)
    data = {'all_data':all_emails}
    return render(request,'client_emails/list_emails.html',data) 

def create_email(request):
    user = request.user
    if request.method == "POST":
        subject=request.POST['subject']
        to=request.POST['to']
        designation=request.POST['designation']
        address=request.POST['address']
        telephone_no=request.POST['telephone_no']
        email_id=request.POST['email_id']
        mobile_no=request.POST['mobile_no']
        website=request.POST['website']
        Leads.objects.create(client_id=user,
                             name=name,
                             company_name=company_name,
                             designation=designation,
                             address=address,
                             telephone_no=telephone_no,
                             email_id=email_id,
                             mobile_no=mobile_no,
                             website=website
                             )
        return HttpResponseRedirect(reverse('client_leads:client/leads'))
    else :
        data={'user':request.user}
        return render(request,'client_leads/add_lead.html',data) 
