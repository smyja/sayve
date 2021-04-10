import os
from decouple import config
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import wallet,Profile,User,sendcoin
from .forms import SignUpForm,TransferForm
from .tokens import account_activation_token
from django.conf import settings
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from buycoins import Wallet
import json
import requests
import random
import decimal


def home_view(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        # url = "https://openapi.rubiesbank.io/v1/createvirtualaccount"

        # payload = "{\n    \"virtualaccountname\": \"Merchant name\",\n    \"amount\": \"1\",\n    \"amountcontrol\": \"VARIABLEAMOUNT\",\n    \"daysactive\": 0,\n    \"minutesactive\": 30,\n    \"callbackurl\": \"https://enxned596fssr.x.pipedream.net\",\n    \"singleuse\":\"N\"\n}"
        # headers = {
        # 'Authorization': 'settings.RUBIES',
        # 'Content-Type': 'application/json'
        # }

        # response = requests.request("POST", url, headers=headers, data=payload)
        # d = json.loads(response.text)
        
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        subject, message, to=[to_email]
            )
            email.send()
            return redirect('activation_sent')
    else:
        form = SignUpForm()
        print(form.errors)
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    
    if request.method == 'POST':
        
        email = request.POST['email']
        password = request.POST['Password']
    
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.success(request, 'This account is disabled')
                return redirect('login')
        else:
            messages.success(request, 'Username or Password is incorrect')
            return redirect('login')
    else:
        context = {}

        return render(request, 'login.html', context)       


def logout_user(request):
    logout(request)
    return redirect('home')



 
@require_http_methods(["GET","POST"])
@csrf_exempt
def webhook(request,slug,id):
    profile = Profile.objects.get(user_id=id)
    data = json.loads(request.body)
    print(data)
    return HttpResponse()


def addbank(request):
    profile = Profile.objects.get(user_id=id)
    wallet_model = wallet()
    print(data)
    return render(request, 'addbank.html')

@login_required(login_url='/login/')
def verifybvn(request):
    if request.method == 'POST':
        trap = request.POST.get('verify')
        print(trap)
        # referenceNo = random.randint(10000, 99999)
        # referencenum = "NAV" + str(referenceNo)
        # print(referencenum)
        # url = "https://openapi.rubiesbank.io/v1/verifybvn"

        # payload = {"bvn":trap,"reference":referencenum}
        # headers = {
        # 'Authorization':settings.RUBIES
        # 
        # response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        # vbvn = json.loads(response.text)
        # print(vbvn)
   
        virtual_user = request.user
        # virtual_user.first_name=vaccount["v"]
        virtual_profile = Profile()
      
        null=None
        jade={"status":"success","message":"BVN-DETAILS","data":{"bvn":"22462625452","first_name":"MARO","middle_name":"TOSHUA","last_name":"AKPOBI","date_of_birth":"10-Jan-2000","phone_number":"09059628124","registration_date":"","enrollment_bank":"","enrollment_branch":"","image_base_64":null,"address":null,"gender":"","email":null,"watch_listed":null,"nationality":"","marital_status":null,"state_of_residence":null,"lga_of_residence":null,"image":null}}
        if (jade["status"])=="success":
            print("We're on track")
            virtual_user.first_name = (jade["data"])["first_name"]
            virtual_user.profile.phone_number=(jade["data"])["phone_number"]
            virtual_user.middle_name =(jade["data"])["middle_name"]
            virtual_user.last_name =(jade["data"])["last_name"]
            virtual_user.save()
            
        else:
            return HttpResponse("Bvn number is invalid")                

             
        return redirect('dashboard')


    return render(request, 'verify.html') 
    
def buycoins(request):
   
  
    auth_key = config("auth_key")
    wallet = Wallet()
    print(wallet)
    usd_coin_address = wallet.create_address(currency="litecoin")
    print(usd_coin_address)
    balances = wallet.get_balances()
    print(balances)
   
    return HttpResponse()   

def transfer(request):
    profile = Profile.objects.get(user=request.user)

    print(profile.username)
    
    if request.method == "POST":
        form = TransferForm(request.POST)
    
        if form.is_valid():
            print(form)
            form.save()
            
            trap = request.POST.get('receiver')
            
            profile2 = Profile.objects.get(username=trap)
            sender = wallet.objects.get(owner=profile)
            
    
            
            receiver = wallet.objects.get(owner=profile2)  # FIELD 1
            print(receiver)
            trx= request.POST.get('amount')
            transfer_amount = trx # FIELD 2
             # FIELD 3
            print(sender.balance)

            # Now transfer the money!
            sender.balance = sender.balance - decimal.Decimal(float(transfer_amount))
            receiver.balance = receiver.balance + decimal.Decimal(float(transfer_amount))

            # Save the changes before redirecting

            return(HttpResponse("Money has been transferred boss!")) 
          #NOTE: Now deleting the instance for future money transactions
        else:
            return(HttpResponse("form is not valid"))    

    else:
        form = TransferForm(initial={"sender": profile.username})
    return render(request, "sendcoins.html", {"form": form})
