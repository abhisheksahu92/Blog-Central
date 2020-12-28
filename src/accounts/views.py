from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate,get_user_model

from .forms import UserLoginForm

# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('username')
        last_name = form.cleaned_data.get('username')
    context = {'form':form,'title':title}
    return render(request,'accounts/login.html',context=context)

def register_view(request):
    context = {}
    return render(request,'accounts/register.html',context=context)

def logout_view(request):
    context = {}
    return render(request,'accounts/logout.html',context=context)
