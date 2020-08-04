from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, VirtualWalletForm
from django.contrib.auth.models import User
from .models import balance

# Create your views here.


def register(request):
    if request.user.is_authenticated:
         return redirect('blog-home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            instance = balance(user=request.user, balance=25)
            instance.save()
            # messages.success(request, f'Account created for {username}!')
            # return redirect('blog-home')
            messages.success(
                request, f'Your account has been created! You are now loggedIn')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        # parameter is passed for filling of form
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your profile has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def virtualWallet(request):
    msg = ""
    if request.method == "POST":
        try:
            username = request.POST["username"]
            amount = request.POST["amount"]
            senderUser = User.objects.get(username=request.user.username)
            receiverrUser = User.objects.get(username=username)
            sender = balance.objects.get(user=senderUser)
            receiverr = balance.objects.get(user=receiverrUser)
            if int(amount) < sender.balance:
                sender.balance = sender.balance - int(amount)
                receiverr.balance = receiverr.balance + int(amount)
                sender.save()
                receiverr.save()
                msg = "Transaction Success"
            else:
                msg = "Please add funds to send more"
        except Exception as e:
            print(e)
            msg = "Transaction Failure, Please check and try again"
    user = balance.objects.get(user=request.user)
    wallet_balance = user.balance
    u_form = VirtualWalletForm()
    context = {
        'u_form': u_form,
        'balance': wallet_balance,
        'msg': msg
    }
    return render(request, 'users/wallet.html', context)
