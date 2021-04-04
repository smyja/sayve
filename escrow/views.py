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
from .models import wallet,Profile,User
from .forms import SignUpForm
from .tokens import account_activation_token
from django.conf import settings
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
import random

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
    return redirect('homepage')



 
@require_http_methods(["GET","POST"])
@csrf_exempt
def webhook(request,slug,id):
    profile = Profile.objects.get(user_id=id)
    data = json.loads(request.body)
    print(data)
    return HttpResponse()



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
        vbvn = json.loads(response.text)
        print(vbvn)
   
        virtual_user = User()
        virtual_user.first_name=vaccount["v"]
        virtual_profile = Profile()        

             
        return redirect('dashboard')


    return render(request, 'verify.html') 
    
    

