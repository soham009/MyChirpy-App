from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import loader
from django.utils.html import strip_tags

from default_email.models import Default_Email
from accounts.models import Portal_User
from lead_manager.models import Leads
from send_email.models import Email_Usage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from default_email.serializer import Default_EmailSerializer

@api_view(['GET',])
def all_default_email(request):
    if request.method == "GET":
        all_emails = Default_Email.objects.all()
        serializer = Default_EmailSerializer(all_emails,many=True)
        return Response(serializer.data)  

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
        email_object = Default_Email.objects.get(pk=email_pk)
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

@login_required(login_url = '/accounts/admin_login')
def default_email(request):
    all_emails = Default_Email.objects.all()
    if request.method == "POST":
        subject = request.POST['subject']
        to = request.POST['to']
        greeting = request.POST['greeting']
        message = request.POST['message']
        thank_you = request.POST['thank_you']
        Default_Email.objects.create(subject=subject,
                                   to=to,
                                    greeting=greeting,
                                    message=message,
                                    thank_you=thank_you)
        return HttpResponseRedirect(reverse('default_email:default_emails'))

    data = {'all_data':all_emails}
    return render(request,'default_email/default_emails.html',data)

def update_email(request,pk):
    email_object = Default_Email.objects.get(pk=pk)
    if request.method == "POST":
        subject = request.POST['subject']
        to = request.POST['to']
        greeting = request.POST['greeting']
        message = request.POST['message']
        thank_you = request.POST['thank_you']
        email_object.subject = subject
        email_object.to = to
        email_object.greeting = greeting
        email_object.message = message
        email_object.thank_you = thank_you
        email_object.save()
        return HttpResponseRedirect(reverse('default_email:default_emails'))

def delete_email(request,pk):
    email_object = Default_Email.objects.get(pk=pk)
    email_object.delete()
    return HttpResponseRedirect(reverse('default_email:default_emails'))
