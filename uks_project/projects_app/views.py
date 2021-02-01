from django.shortcuts import render, redirect
from django.http import HttpResponse
from projects_app.models import Project, Column
from issues_app.models import Issue
from projects_app.forms import ProjectForm, ColumnForm
import sys
import io

# Create your views here.
def main(request):
    projects = Project.objects.all().order_by('id')
    projects_dict = { 'projects': projects}
    return render(request, 'projects_app/main.html', projects_dict)

def new_project(request):
    form = ProjectForm()

    if request.method =='POST' :
        form = ProjectForm(request.POST)

        if form.is_valid(): 
            project = Project()
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.status = 'Open'

            project.save()

            return redirect('/projects')
    
    return render(request,'projects_app/new_project.html',{'form': form})


def project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects')
    

    objects_dict = {
        'project':project, 
        'columns': project.columns.all(),
        'issues': Issue.objects.all()
    }
    return render(request,"projects_app/project.html",objects_dict)


def edit_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects')

    form = ProjectForm(instance=project)

    if request.method =='POST' :
        form = ProjectForm(request.POST)

        if form.is_valid(): 
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']

            project.save()

            return redirect('/projects')
            
    return render(request,'projects_app/new_project.html',{'form': form})


def close_project(request,project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects')
    project.status = "Closed"
    project.save()

    return redirect('/projects')


def reopen_project(request,project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects')
    project.status = "Open"
    project.save()

    return redirect('/projects')


def delete_project(request,project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects')
    project.delete()

    return redirect('/projects')


def new_column(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects')

    form = ColumnForm()

    if request.method =='POST' :
        form = ColumnForm(request.POST)

        if form.is_valid(): 
            column = Column()
            column.name = form.cleaned_data['name']
            column.project = project 

            column.save()

            return redirect('/projects/'+ str(project_id))

    objects_dict = {
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    
    return render(request,'projects_app/new_column.html',objects_dict)


def edit_column(request, project_id, column_id):
    try:
        column = Column.objects.get(id=column_id)
    except:
        return redirect('/projects/'+ str(project_id))

    try:
        project = Project.objects.get(id=project_id)
    except:
        return redirect('/projects/'+ str(project_id))


    form = ColumnForm(instance=column)

    if request.method =='POST' :
        form = ColumnForm(request.POST)

        if form.is_valid(): 
            column.name = form.cleaned_data['name']

            column.save()

            return redirect('/projects/'+ str(project_id))

    objects_dict = {
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    
    return render(request,'projects_app/new_column.html',objects_dict)


def delete_column(request,project_id, column_id):
    try:
        column = Column.objects.get(id=column_id)
    except:
        return redirect('/projects/'+ str(project_id))
    
    column.delete()

    return redirect('/projects/' + str(project_id))

def remove_issue(request,project_id, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
    except:
        return redirect('/projects/'+ str(project_id))
    
    issue.column = None
    issue.save()
    
    return redirect('/projects/' + str(project_id))
