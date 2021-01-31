from django.shortcuts import render
from django.http import HttpResponse
from projects_app.models import Project, Column
import sys
import io

# Create your views here.
def main(request):
    projects = Project.objects.all()
    projects_dict = { 'projects': projects}
    return render(request, 'projects_app/main.html', projects_dict)

def new_project(request):
    return render(request,'projects_app/new_project.html')