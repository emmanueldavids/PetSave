from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import wallet, Donation
from .forms import SignUpForm,DonationForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index.html')

@login_required
def dashboard(request):
    # user = request.user
    money = wallet.objects.get(id= 1)
    donation = Donation.objects.filter()
    
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
    money = wallet.objects.get(id=1)

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


# def donate(request):
#     user = request.user
#     Wallet = None
#     if request.method == 'POST':
#         form = DonationForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             # Create a wallet for the user if it doesn't exist
#             Wallet, created = wallet.objects.get_or_create(balance=100.00)
#             if Wallet.balance >= amount:
#                 Wallet.balance -= amount
#                 Wallet.save()
#                 form.save()
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, 'Insufficient balance')
#         else:
#             # Form is not valid, render with error messages
#             return render(request, 'donate.html', {'form': form})
#     else:
#         form = DonationForm()

#     return render(request, 'donate.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.balance = Decimal('100.00')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            messages.success(request, "Account was created for " + username)
            return redirect('login')
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
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
