from django.shortcuts import render, redirect
from django.http import HttpResponse
from projects_app.models import Project, Column
from projects_app.forms import ProjectForm
import sys
import io

# Create your views here.
def main(request):
    projects = Project.objects.all().order_by('id')
    projects_dict = { 'projects': projects}
    return render(request, 'projects_app/main.html', projects_dict)

def new_project(request):
    projects = Project.objects.all().order_by('id')
    form = ProjectForm()

    if request.method =='POST' :
        form = ProjectForm(request.POST)

        if form.is_valid(): 
            project = Project()
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.status = 'Open'

            project.save()

            return render(request, 'projects_app/main.html' ,{'projects':projects})
            
    return render(request,'projects_app/new_project.html',{'form': form})

def close_project(request,project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return render(request,'projects_app/main.html',{'projects': projects})
    project.status = "Closed"
    project.save()
    projects = Project.objects.all().order_by('id')

    return redirect('/projects')

def reopen_project(request,project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return render(request,'projects_app/main.html',{'projects': projects})
    project.status = "Open"
    project.save()
    projects = Project.objects.all().order_by('id')

    return redirect('/projects')
