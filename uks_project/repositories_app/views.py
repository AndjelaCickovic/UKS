from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
def main(request):
    return render(request, 'repositories_app/repositories.html')