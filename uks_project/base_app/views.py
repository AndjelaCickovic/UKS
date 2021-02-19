from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request,'base_app/base.html')

def index(request):
    return render(request,'base_app/index.html')