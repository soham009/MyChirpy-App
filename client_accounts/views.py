from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from accounts.models import Portal_User
import urllib.request
import json
import random
from accounts.send_sms import replaceSpaces
from django.contrib.auth import logout, authenticate, login as check_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
def client_signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        Mobile_No = request.POST['Mobile_No']
        email = request.POST ['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'client_accounts/signup.html',{'error_message':'Passwords do not match!'})
        if Portal_User.objects.filter(username = Mobile_No).exists():
            return render(request, 'client_accounts/signup.html',{'error_message':'Username already exists!'})
        else:
            number = random.randint(1000,9999) 
            user = Portal_User.objects.create(first_name = first_name,
                                             username=Mobile_No,
                                             Mobile_No=Mobile_No,
                                             email = email,
                                             Otp = number,
                                             password= make_password(password),
                                             user_role=2)
            return HttpResponseRedirect(reverse('client_accounts:client/login'))
    else:
        return render(request, 'client_accounts/signup.html')

def client_login(request):
    if request.method == 'POST':
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.Varified == False:
                    message = "Your One Time Password (OTP) for Visiting card App is :" +str(user.Otp)
                    data = {'user':user}
                    return render(request,'client_accounts/otp.html',data)
                else:
                    check_login(request, user)
                    user = request.user
                    if user.user_role == 2:
                        return HttpResponseRedirect(reverse('client_leads:client/leads'))
                    else:
                        return render(request, 'client_accounts/login.html',{'error_message': 'Invalid User!'})    
        else:
            return render(request, 'client_accounts/login.html',{'error_message': 'Username or Password Incorrect!'})
    else:
        return render(request,'client_accounts/login.html')

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

def client_validation(request):
    if request.method == "POST":
        Otp = request.POST['Otp']
        pk = request.POST['pk']
        user = Portal_User.objects.get(pk=pk)
        if user.Otp == Otp:
            user.Varified = True
            user.save()
            check_login(request, user)
            return HttpResponseRedirect(reverse('client_leads:client/leads'))
        else:
            number = random.randint(1000,9999)
            user.Otp = number
            user.save()
            return HttpResponseRedirect(reverse('client_accounts:client/login'))

# @api_view(['POST',])
# def registration_view(request):

#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response']="User successfully registered"
#         else:
#             data = serializer.errors
#         return Response(data)