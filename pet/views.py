from decimal import Decimal
from http.client import HTTPResponse
import random
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import OtpToken, wallet, Donation, SignUp
from .forms import SignUpForm,DonationForm
from django.template.response import TemplateResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout




def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def logout(request):
    if request.method == 'POST':
        logout(request)
        request.session.delete()
        return redirect('index.html')

@login_required
def dashboard(request):
    donation = Donation.objects.filter()
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    money = wallet.objects.get()
 
    for donate in donation:
        amount = donate.amount
    

    prev_amount = amount + money.balance



    donations = Donation.objects.all()
    paginator = Paginator(donations, 5)  # Show 5 donations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'balance': money.balance,
        'amount':amount,
        'prev_balance': prev_amount,
        'page_obj': page_obj,
    }
    return render(request, 'dashboard.html', context)
    # request.user.id = request.user


def donate(request):
    user = request.user
    money = wallet.objects.get()

    if request.method == 'POST':
        user = DonationForm(request.POST)
        amount = Decimal(request.POST['amount'])

        if money.balance >= amount:
            money.balance -= amount
            money.save()
            user.save()
            return redirect('dashboard')
        else:
            messages.error(request, 'Insufficient balance')
    form = DonationForm()
    return render(request, 'donate.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_activate = False
            user.balance = Decimal('100.00')
            user.save()
            send_otp(user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            messages.success(request, "Account was created for " + username + "An OTP was sent to your Email")
            return redirect('sent_otp', username=request.POST['username'])
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_verified:
                auth_login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials or unverified account")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def send_otp(user):
    otp_code = str(random.randint(100000, 999999))
    OtpToken.objects.create(user=user, otp_code=otp_code)
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    send_mail(subject, message, from_email, [to_email], fail_silently=False)

def verify_otp(request, user_id, otp_code):
    user = SignUp.objects.get(id=user_id)
    otp_token = OtpToken.objects.filter(user=user, otp_code=otp_code).last()
    if otp_token and otp_token.created_at + timezone.timedelta(minutes=5) > timezone.now():
        user.is_verified = True
        user.save()
        return redirect('login')
    return HTTPResponse('Invalid OTP')
