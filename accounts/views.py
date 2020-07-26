from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# ,permission_classes
# from rest_framework.permissions import IsAuthenticated
from accounts.send_sms import replaceSpaces
import urllib.request
import urllib.parse
import random
import json
from accounts.serializer import UserSerializer
from accounts.models import Portal_User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password

from django.contrib.auth import logout, authenticate, login as check_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from send_sms.models import SMS_Usage
from send_email.models import Email_Usage
from lead_manager.models import Leads
from email_manager.models import EmailMaster
# Create your views here.

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        email=request.POST['email']
        #username=request.POST['username']
        Mobile_No=request.POST['Mobile_No']
        password=request.POST['password']
        number = random.randint(1000,9999)
        try:
            user = Portal_User.objects.get(username=username)
        except Portal_User.DoesNotExist:
            user = None
        if user is None:
            account = Portal_User.objects.create(
                first_name=first_name,
                email=email,
                username=Mobile_No,
                Mobile_No=Mobile_No,
                password = make_password(password),
                account_type = False,
                user_role = 2,
                Otp = number
            )
            return Response({
                'message': "User Successfully created"
                })
        else :
            return Response({
                'message': "Username already exists"
                })

@api_view(['POST',])
def user_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({
                'pk':user.pk,
                'message': "Successfully Login"
                })
        else :
            return Response({
                'message': "Login Failed !!!"
                })



#if account_models.Portal_User.objects.filter(username=username, password=make_password(password)).exists():
#if
#            user = Portal_User.objects.get(username=username, password=make_password(password))
#            return Response({
#                'pk':user.pk,
#                'message': "Successfully Login"
#                })
#        else:
#            return Response({
#                'message': "Login Failed !!!"
#                })

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.Varified == False:
            message = "Your One Time Password (OTP) for Visiting card App is :" +str(user.Otp)
            f1 = urllib.request.urlopen("https://www.volshebnypnstatement.in/my_gov_app?mobile_one="+str(user.Mobile_No)+"&otp_code="+str(user.Otp))
            # message_urlify = replaceSpaces(message)
            # api_call1 = urllib.request.Request("http://vas.hexaroute.com/api.php?username=volshebny&password=pass1234&route=1&sender=VOLSHY&mobile[]="+number1+"&message[]="+message_urlify)
            # f = urllib.request.urlopen(api_call1)
            # if f.read() != b'Please enter mobile no.':
            #     user.Varified == True
            #     user.save()
            return Response({
                'pk':user.pk,
                'message': "Sent Verification Code"
            })
        else:
            return Response({
                'pk':user.pk,
                'message': "Successfully Login"
            })

@api_view(['POST',])
# @permission_classes([IsAuthenticated])
def otp_submit(request):
    if request.method == "POST":
        Otp = request.POST['Otp']
        pk = request.POST['pk']
        user = Portal_User.objects.get(pk=pk)
        if user.Otp == Otp:
            user.Varified = True
            user.save()
            return Response({
                'message': "Varified successfully"
            })
        else:
            number = random.randint(1000,9999)
            user.Otp = number
            user.save()
            return Response({
                'message': "UnVarified User"
            })


def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

def admin_login(request):
    if request.method == 'POST':
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                check_login(request, user)
                user = request.user
                if user.user_role == 1:
                    return HttpResponseRedirect(reverse('accounts:dashboard'))
                else:
                    return render(request, 'accounts/login.html',{'error_message': 'Invalid User!'})
        else:
            return render(request, 'accounts/login.html',{'error_message': 'Username or Password Incorrect!'})
    else:
        return render(request,'accounts/login.html')

@login_required(login_url = '/accounts/admin_login')
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:admin_login'))

@login_required(login_url = '/accounts/admin_login')
def clients(request):
    all_data = Portal_User.objects.filter(user_role=2)
    data = {'all_data':all_data}
    return render(request,'accounts/client_master.html',data)

@login_required(login_url = '/accounts/admin_login')
def dashboard(request):
    all_data = Portal_User.objects.filter(user_role=2).order_by("-date_joined")
    all_send_sms = SMS_Usage.objects.all().count()
    all_send_email = Email_Usage.objects.all().count()
    all_clients = Portal_User.objects.filter(user_role=2).all().count()
    all_leads = Leads.objects.all().count()
    all_converted = Email_Usage.objects.filter(lead_status="Converted").all().count()
    all_emails = EmailMaster.objects.all().count()
    data = {'all_data':all_data[0:6],'all_send_sms':all_send_sms,'all_clients':all_clients,'all_leads':all_leads,
    'all_converted':all_converted,'all_emails':all_emails,'all_send_email':all_send_email}
    return render(request,'accounts/dashboard.html',data)

@login_required(login_url = '/accounts/admin_login')
def all_users(request):
    all_data = Portal_User.objects.all()
    if request.method == "POST":
        first_name = request.POST['first_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_role = request.POST['user_role']
        Mobile_No = request.POST['Mobile_No']
        if user_role == "Client":
            Otp = random.randint(1000,9999)
            role = 2
        else:
            Otp = ""
            role = 1
        if Portal_User.objects.filter(username=username).exists():
            data = {'all_data':all_data,'error_message':'Username already exists!'}
            return render(request,'accounts/user_master.html',data)
        else:
            user = Portal_User.objects.create(first_name=first_name,
                                                username= username,
                                                email=email,
                                                user_role = role,
                                                password=make_password(password),
                                                Otp = Otp,
                                                Mobile_No = Mobile_No)
    data = {'all_data':all_data}
    return render(request, 'accounts/user_master.html',data)

@login_required(login_url = '/accounts/admin_login')
def delete_user(request,pk):
    user = Portal_User.objects.get(pk=pk)
    user.delete()
    return HttpResponseRedirect(reverse('accounts:users'))

@login_required(login_url = '/accounts/admin_login')
def update_user(request,pk):
    if request.method == "POST":
        first_name = request.POST['first_name']
        password = request.POST['password']
        email = request.POST['email']
        user = Portal_User.objects.get(pk=pk)
        user.first_name = first_name
        user.email = email
        user.password = make_password(password)
        user.save()
        return HttpResponseRedirect(reverse('accounts:users'))

@login_required(login_url = '/accounts/admin_login')
def client_dashboard(request,pk):
    user = Portal_User.objects.get(pk=pk)
    all_send_sms = SMS_Usage.objects.filter(send_from = user).all().count()
    all_send_email = Email_Usage.objects.filter(send_from = user).all().count()
    all_leads = Leads.objects.filter(client_id=user).all().count()
    all_converted = Email_Usage.objects.filter(send_from = user,lead_status="Converted").all().count()
    all_emails = EmailMaster.objects.filter(client_id=user).all().count()
    all_data = Leads.objects.filter(client_id = user).order_by('-created_at')
    data = {'user':user,'all_data':all_data[0:6],'all_send_sms':all_send_sms,'all_leads':all_leads,
    'all_converted':all_converted,'all_emails':all_emails,'all_send_email':all_send_email}

    return render(request, 'accounts/client_dashboard.html',data)
