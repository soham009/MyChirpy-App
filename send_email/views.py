from django.shortcuts import render
from lead_manager.models import Leads
from email_manager.models import EmailMaster

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import Portal_User
from email_manager.serializer import EmailSerializer
from lead_manager.serializer import LeadSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import loader
from django.utils.html import strip_tags
from send_email.models import Email_Usage
from send_email.serializer import Email_UsageSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@api_view(['GET',])
def bulk_email_data(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = {}
        all_leads = Leads.objects.filter(client_id=user)
        all_emails = EmailMaster.objects.filter(client_id=user)
        serializer1 = LeadSerializer(all_leads,many=True)
        serializer2 = EmailSerializer(all_emails,many=True)
        data['leads']= serializer1.data
        data['email']= serializer2.data
        return Response(data)

@api_view(['POST',])
def send_bulk_email(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        data = {}
        email_pk = request.POST['email_pk']
        leads_list = request.POST.getlist('select_lead')
        email_object = EmailMaster.objects.get(pk=email_pk)
        subject = email_object.subject
        message = email_object.message
        html_message = loader.render_to_string(
                'send_email/e_msg.html',
                {
                    'to':email_object.to,
                    'greeting':email_object.greeting,
                    'message': email_object.message,
                    'thank_you':email_object.thank_you
                }
            )
        for lead in leads_list:
            lead_object = Leads.objects.get(pk=lead)   
            email = lead_object.email_id
            
            text_content = strip_tags(html_message)
            # send_mail(subject,'finitytechserv@gmail.com',[email],fail_silently=True,html_message=html_message)
            send_mail(subject,message,'finitytechserv@gmail.com',[email],fail_silently=True,html_message=html_message)
            # mail.send()
            Email_Usage.objects.create(lead_name = lead_object.name,
                                       lead_email = email,
                                       send_from = user,
                                       status = "success",)
        data['response']="Email Send Successfully"
        return Response(data)   

@api_view(['GET',])
def all_send_email_leads(request,pk):
    try:
        user = Portal_User.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        all_send_email = Email_Usage.objects.filter(send_from=user)
        serializer = Email_UsageSerializer(all_send_email,many=True)
        return Response(serializer.data)

@api_view(['POST',])
def update_lead_status(request,pk):
    try:
        send_email = Email_Usage.objects.get(pk=pk)
    except Portal_User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        data = {}
        lead_status = request.POST['lead_status']
        send_email.lead_status = lead_status
        send_email.save()
        data['response']="Status Updated Successfully"
        return Response(data)
        
@login_required(login_url = '/accounts/admin_login')
def all_send_email_to_lead(request,pk):
    user = Portal_User.objects.get(pk=pk)
    all_data = Email_Usage.objects.filter(send_from=user)
    data = {'all_data':all_data,'user':user}
    return render(request,'send_email/send_email_master.html',data)


        