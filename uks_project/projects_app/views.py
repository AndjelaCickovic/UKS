from django.shortcuts import render
from django.http import HttpResponse
import sys
import io

# Create your views here.
def main(request):
    return render(request, 'projects_app/main.html')