from django.shortcuts import render,redirect
from users.forms import UserForm,EditUserForm
from django.template import RequestContext

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

from users.models import AppUser

# Create your views here.
def register(request):
    
    registered = False
    
    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            app_user = AppUser.objects.create(user=user)

            if 'profile_picture' in request.FILES:  
                app_user.profile_picture = request.FILES['profile_picture']

            app_user.save()

            registered = True
            return render(request,"users/login.html",{'registered':registered})
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
                return redirect('/repositories')
            else:
                return render(request,'users/login.html',{'err':'Account not active!'})

        else:
            return render(request,'users/login.html',{'error':'Invalid login details supplied!'})
    else:
        return render(request,'users/login.html',{})

@login_required
def user_logut(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def edit_profile(request):

    form = EditUserForm(instance=request.user)
    user = request.user

    app_user = AppUser.objects.get(user=user)

    obj_dict ={
        'form':form,
        'profile_picture' : app_user.profile_picture
    }

    if request.method == 'POST':
        
        form = EditUserForm(data=request.POST,instance=request.user)
        obj_dict['form']=form
        if form.is_valid():

            if 'profile_picture' in request.FILES:  
                app_user.profile_picture = request.FILES['profile_picture']
                obj_dict['profile_picture']=app_user.profile_picture
                app_user.save()
            
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['password']


            if old_password:
                user = form.save(commit=False)
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                obj_dict['success_message'] = 'Data successfully updated.'
            else:
                user = form.save(commit=False)
                user.save()
                obj_dict['success_message'] = 'Data successfully updated.'

    return render(request,'users/edit_profile.html',obj_dict)