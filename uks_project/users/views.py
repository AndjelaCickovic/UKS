from django.shortcuts import render,redirect
from users.forms import UserForm
from django.template import RequestContext

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.
def register(request):
    
    registered = False
    
    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            print('user registered')
            registered = True
            return render(request,"users/login.html",{})
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,'users/registration.html',
                            {'user_form':user_form,
                            'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Login failed")
            return HttpResponse("Invalid login detils supplied!")
    else:
        return render(request,'users/login.html',{})

@login_required
def user_logut(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
