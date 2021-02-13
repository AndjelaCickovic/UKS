from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from projects_app.models import Project, Column
from issues_app.models import Issue
from issues_app.forms import IssueForm
from users.models import AppUser
from repositories_app.models import Repository, RepositoryUser
from projects_app.forms import ProjectForm, ColumnForm, IssueColumnForm, CustomMCF
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


import sys
import io


def get_role(request, repository):
    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)
            repository_user = RepositoryUser.objects.get(user=app_user, repository=repository)
            return True
        except:
            return False
    else:
        return False
    
def main(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)
    if repository.is_public == False and role == False:
        return redirect('/repositories')

    objects_dict = { 
        'projects': repository.projects.all(),
        'repository': repository,
        'role': role
        }

    return render(request, 'projects_app/main.html', objects_dict)

@login_required
def new_project(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ProjectForm(initial={'repository':repository})

    if request.method =='POST' :
        form = ProjectForm(request.POST)

        if form.is_valid(): 
            project = Project()
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.repository = repository
            project.status = 'Open'

            project.save()
            return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))
    
    return render(request,'projects_app/new_project.html',{'repository': repository,'form': form})


def project(request, project_id,repository_id):
    try:
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'role': role
    }
    return render(request,"projects_app/project.html",objects_dict)

@login_required
def edit_project(request, project_id,repository_id):
    try:
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ProjectForm(instance=project,initial={'project': project})

    if request.method =='POST' :
        form = ProjectForm(request.POST)

        if form.is_valid(): 
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']

            project.save()

            return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))
            
    return render(request,'projects_app/new_project.html',{'repository': repository,'form': form})

@login_required
def close_project(request,project_id, repository_id):
    try:
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    project.status = "Closed"
    project.save()
    
    return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

@login_required
def reopen_project(request,project_id,repository_id):
    try:
        project = Project.objects.get(id=project_id)       
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    project.status = "Open"
    project.save()

    return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

@login_required
def delete_project(request,project_id,repository_id):
    try:
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    project.delete()

    return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

@login_required
def new_column(request, repository_id, project_id):
    try:
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ColumnForm(initial={'project': project})

    if request.method =='POST' :
        form = ColumnForm(request.POST)

        if form.is_valid(): 
            column = Column()
            column.name = form.cleaned_data['name']
            column.project = project 

            column.save()

            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    
    return render(request,'projects_app/new_column.html',objects_dict)

@login_required
def edit_column(request, repository_id, project_id, column_id):
    try:
        column = Column.objects.get(id=column_id)
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home') 

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ColumnForm(instance=column,initial={'project': project})

    if request.method =='POST' :
        form = ColumnForm(request.POST)

        if form.is_valid(): 
            column.name = form.cleaned_data['name']

            column.save()

            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    
    return render(request,'projects_app/new_column.html',objects_dict)

@login_required
def delete_column(request, repository_id, project_id, column_id):
    try:
        column = Column.objects.get(id=column_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    column.delete()

    return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

@login_required
def remove_issue(request, repository_id, project_id, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    issue.column = None
    issue.save()
    
    return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

@login_required
def edit_issue(request, repository_id, project_id, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')    

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = IssueForm(instance=issue)

    if request.method =='POST' :
        form = IssueForm(request.POST)

        if form.is_valid(): 
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.save()
            # issue.column = column
            issue.labels.set(form.cleaned_data['labels'])
            issue.assignees.set(form.cleaned_data['assignees'])
            issue.repository = repository
            issue.save()
            
            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))
            
    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    return render(request, 'projects_app/new_issue.html', objects_dict)


@login_required
def change_column_issue(request, repository_id, project_id, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')   

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    columns = project.columns.all()
    form = IssueColumnForm(instance=issue,initial={'columns':issue.column.id})
    form.fields['columns'] = CustomMCF(queryset=columns,empty_label=None)
    if request.method =='POST' :
        form = IssueColumnForm(request.POST)

        if form.is_valid(): 
            issue.column = form.cleaned_data['columns']
            issue.save()
            
            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))
            
    objects_dict = {
        'repository' : repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    return render(request, 'projects_app/new_issue.html', objects_dict)


@login_required
def delete_issue(request, repository_id, project_id, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    issue.delete()
            
    return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))


@login_required
def new_issue(request, repository_id, project_id, column_id):
    try:
        project = Project.objects.get(id=project_id)
        repository = Repository.objects.get(id=repository_id)
        column = Column.objects.get(id=column_id)
    except:
        return redirect('/home')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = IssueForm()

    if request.method =='POST' :
        form = IssueForm(request.POST)

        if form.is_valid(): 
            issue = Issue()
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.save()
            issue.column = column
            issue.labels.set(form.cleaned_data['labels'])
            issue.assignees.set(form.cleaned_data['assignees'])
            issue.repository = repository
            issue.save()
            
            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))
            
    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form
    }
    return render(request, 'projects_app/new_issue.html', objects_dict)