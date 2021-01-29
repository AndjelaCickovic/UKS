from django.shortcuts import render,redirect
from users.forms import UserForm

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
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,'users/registration.html',
                            {'user_form':user_form,
                            'registered':registered})

def login(request):
    return render(request,'users/login.html')