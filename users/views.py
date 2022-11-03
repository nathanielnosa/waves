from django.shortcuts import redirect, render

# Create your views here.
from . forms import CustomerProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate

from stores.models import Order

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    customer = CustomerProfile()

    if request.method == 'POST':
        form = CustomerProfile(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(username = username):
                messages.warning(request, 'Username already exist')
                return redirect('register')
            if User.objects.filter(email = email)   :
                messages.warning(request, 'Email already exist')
                return redirect('register')
            if password != password2:
                messages.warning(request, 'password not match')
                return redirect('register')

            user = User.objects.create_user(username,email,password)
            form = form.save(commit=False)
            form.user = user

            form.save()
            return redirect('login')
    context = {
        'form':customer
    }
    return render(request, 'users/register.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password= request.POST.get('pwd')

        user = authenticate(username = username , password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully')
            if "next" in request.GET:
                next_url=request.GET.get("next")
                return redirect(next_url)
            else:
                return redirect('home')
            
        else:
            messages.warning(request, 'Invalid Username/Password')
    return render(request, 'users/login.html')


def logoutuser(request):
    logout(request)
    messages.success(request, 'User logged out successfully')
    return redirect('login')


def dashboard(request):
    profile = request.user.customer
    orders = Order.objects.filter(cart__customer = profile)
    context ={
        'profile':profile,
        'orders':orders
    }
    return render(request, 'users/dashboard.html',context)