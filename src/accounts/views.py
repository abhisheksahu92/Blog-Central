from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate,get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm,UserRegisterForm

# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username,password = password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('posts:postindex'))
        else:
            messages.error(request,'Invalid Credentials')
            return HttpResponseRedirect(reverse('accounts:login'))

    context = {'form':form,'title':title}
    return render(request,'accounts/login.html',context=context)

def register_view(request):
    registered = False
    form = UserRegisterForm(request.POST or None)
    title = 'Register'
    if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email    = form.cleaned_data.get('email')
            first_name    = form.cleaned_data.get('first_name')
            last_name    = form.cleaned_data.get('last_name')
            if User.objects.filter(username=username).exists():
                messages.success(request,'User already exits. Please Login')
            else:
                User.objects.create_user(
                    username = username,
                    email=email,
                    password=password,
                    first_name = first_name,
                    last_name = last_name

                )
                messages.success(request,'Registration is Done.')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        print(form.errors)

    context = {'form':form,'registered':registered,'title':title}
    return render(request,'accounts/register.html',context=context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('posts:postindex'))
