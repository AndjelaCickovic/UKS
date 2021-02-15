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
from django.core.cache import cache


import sys
import io

def projects_key(repository_id):
    return "projects.all." + str(repository_id)

def project_key(id):
    return "project."+str(id)

def repository_key(id):
    return "repository."+str(id)

def issue_key(id):
    return "issue."+str(id)

def column_key(id):
    return "column."+str(id)


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
    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    role = get_role(request, repository)
    if repository.is_public == False and role == False:
        return redirect('/repositories')

    projects = get_projects_from_cache(repository)

    objects_dict = { 
        'projects': projects,
        'repository': repository,
        'role': role
        }

    return render(request, 'projects_app/main.html', objects_dict)

@login_required
def new_project(request, repository_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ProjectForm(initial={'repository':repository})

    if request.method =='POST' :
        form = ProjectForm(request.POST,initial={'repository':repository})

        if form.is_valid(): 
            project = Project()
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.repository = repository
            project.status = 'Open'

            project.save()

            remove_projects_from_cache(repository_id)

            return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

    return render(request,'projects_app/new_project.html',{'repository': repository,'form': form})


def project(request, project_id,repository_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    project = get_project_from_cache(project_id)
    if not project:
        return redirect('/repositories')

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
    
    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    project = get_project_from_cache(project_id)
    if not project:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ProjectForm(instance=project,initial={'project': project})

    if request.method =='POST' :
        form = ProjectForm(request.POST,instance=project,initial={'project':project})

        if form.is_valid(): 
            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']

            project.save()
            remove_project_from_cache(project_id)
            remove_projects_from_cache(repository_id)
            return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))
            
    return render(request,'projects_app/new_project.html',{'repository': repository,'form': form})

@login_required
def close_project(request,project_id, repository_id):
    
    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    project = get_project_from_cache(project_id)
    if not project:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    project.status = "Closed"
    project.save()
    remove_projects_from_cache(repository_id)
    remove_project_from_cache(project_id)
    
    return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

@login_required
def reopen_project(request,project_id,repository_id):
    
    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    project = get_project_from_cache(project_id)
    if not project:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    project.status = "Open"
    project.save()
    remove_project_from_cache(project_id)
    remove_projects_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

@login_required
def delete_project(request,project_id,repository_id):
    
    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    project = get_project_from_cache(project_id)
    if not project:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    project.delete()
    remove_project_from_cache(project_id)
    remove_projects_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:projects_app:main', kwargs={'repository_id':repository_id}))

@login_required
def new_column(request, repository_id, project_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    project = get_project_from_cache(project_id)
    if not project:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ColumnForm(initial={'project': project})

    if request.method =='POST' :
        form = ColumnForm(request.POST,initial={'project': project})

        if form.is_valid(): 
            column = Column()
            column.name = form.cleaned_data['name']
            column.project = project 

            column.save()
            remove_project_from_cache(project_id)
            remove_projects_from_cache(repository_id)

            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form,
        'role': role
    }
    
    return render(request,'projects_app/new_column.html',objects_dict)

@login_required
def edit_column(request, repository_id, project_id, column_id):

    column = get_column_from_cache(column_id)
    project = get_project_from_cache(project_id)
    repository = get_repository_from_cache(repository_id)
    
    if not column or not project or not repository:
        return redirect('/repositories') 

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = ColumnForm(instance=column,initial={'project': project})

    if request.method =='POST' :
        form = ColumnForm(request.POST,instance=column,initial={'project': project})

        if form.is_valid(): 
            column.name = form.cleaned_data['name']

            column.save()
            remove_column_from_cache(column_id)
            remove_project_from_cache(project_id)
            remove_projects_from_cache(repository_id)

            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form,
        'role': role
    }
    
    return render(request,'projects_app/new_column.html',objects_dict)

@login_required
def delete_column(request, repository_id, project_id, column_id):

    column = get_column_from_cache(column_id)
    project = get_project_from_cache(project_id)
    repository = get_repository_from_cache(repository_id)
    
    if not column or not project or not repository:
        return redirect('/repositories') 

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    column.delete()
    remove_column_from_cache(column_id)
    remove_project_from_cache(project_id)
    remove_projects_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

@login_required
def remove_issue(request, repository_id, project_id, issue_id):
    
    issue = get_issue_from_cache(issue_id)
    repository = get_repository_from_cache(repository_id)
    
    if not issue or not repository:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    column_id = issue.column.id

    issue.column = None
    issue.save()
    
    remove_issue_from_cache(issue_id)
    remove_column_from_cache(column_id)
    remove_project_from_cache(project_id)
    remove_projects_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

@login_required
def edit_issue(request, repository_id, project_id, issue_id):

    issue = get_issue_from_cache(issue_id)
    repository = get_repository_from_cache(repository_id)
    project = get_project_from_cache(project_id)
    
    if not issue or not repository or not project:
        return redirect('/repositories') 

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = IssueForm(instance=issue, repository = repository)

    if request.method =='POST' :
        form = IssueForm(request.POST, repository = repository)

        if form.is_valid(): 
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.save()
            issue.labels.set(form.cleaned_data['labels'])
            assignees = []
            for user in form.cleaned_data['assignees']:
                print(user.user)
                assignees.append(user.user)
            issue.assignees.set(assignees)
            issue.repository = repository
            issue.save()

            remove_issue_from_cache(issue_id)
            remove_column_from_cache(issue.column.id)
            remove_project_from_cache(project_id)
            remove_projects_from_cache(repository_id)
            
            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))
            
    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form,
        'role': role
    }
    return render(request, 'projects_app/new_issue.html', objects_dict)

@login_required
def change_column_issue(request, repository_id, project_id, issue_id):
    
    issue = get_issue_from_cache(issue_id)
    repository = get_repository_from_cache(repository_id)
    project = get_project_from_cache(project_id)
    
    if not issue or not repository or not project:
        return redirect('/repositories') 

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

            remove_issue_from_cache(issue_id)
            remove_column_from_cache(issue.column.id)
            remove_project_from_cache(project_id)
            remove_projects_from_cache(repository_id)
            
            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))
            
    objects_dict = {
        'repository' : repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form,
        'role': role
    }
    return render(request, 'projects_app/new_issue.html', objects_dict)

@login_required
def delete_issue(request, repository_id, project_id, issue_id):
    
    issue = get_issue_from_cache(issue_id)
    repository = get_repository_from_cache(repository_id)
    
    if not issue or not repository:
        return redirect('/repositories') 

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    column_id = issue.column.id
    issue.delete()
    remove_issue_from_cache(issue_id)
    remove_column_from_cache(column_id)
    remove_project_from_cache(project_id)
    remove_projects_from_cache(repository_id)
            
    return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))

@login_required
def new_issue(request, repository_id, project_id, column_id):

    column = get_column_from_cache(column_id)
    project = get_project_from_cache(project_id)
    repository = get_repository_from_cache(repository_id)
    
    if not column or not project or not repository:
        return redirect('/repositories')

    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    form = IssueForm(repository= repository)

    if request.method =='POST' :
        form = IssueForm(request.POST, repository = repository)

        if form.is_valid(): 
            issue = Issue()
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.save()
            issue.column = column
            issue.labels.set(form.cleaned_data['labels'])
            assignees = []
            for user in form.cleaned_data['assignees']:
                print(user.user)
                assignees.append(user.user)
            issue.assignees.set(assignees)
            issue.repository = repository
            issue.save()
            
            remove_column_from_cache(column_id)
            remove_project_from_cache(project_id)
            remove_projects_from_cache(repository_id)
            return HttpResponseRedirect(reverse('repositories_app:projects_app:project', kwargs={'project_id': project_id,'repository_id':repository_id}))
            
    objects_dict = {
        'repository': repository,
        'project':project, 
        'columns': project.columns.all(),
        'form': form,
        'role': role
    }
    return render(request, 'projects_app/new_issue.html', objects_dict)

def get_repository_from_cache(repository_id):
    repository = cache.get(repository_key(repository_id))
    if not repository:
        try:
            repository = Repository.objects.get(id=repository_id)
        except:
            return None
        cache.set(repository_key(repository_id),repository)
    return repository

def get_projects_from_cache(repository):
    projects = cache.get(project_key(repository.id))
    if not projects:
        projects = Project.objects.filter(repository=repository).order_by('id')
        print(projects)
        cache.set(project_key(repository.id),projects)
    return projects

def remove_projects_from_cache(repository_id):
    cache.delete(project_key(repository_id))

def get_project_from_cache(project_id):
    project = cache.get(project_key(project_id))
    if not project:
        try:
            project = Project.objects.get(id=project_id)
        except:
            return None
        cache.set(project_key(project_id),project)
    return project

def remove_project_from_cache(project_id):
    cache.delete(project_key(project_id))

def get_column_from_cache(column_id):
    column = cache.get(column_key(column_id))
    if not column:
        try:
            column = Column.objects.get(id=column_id)
        except:
            return None
        cache.set(column_key(column_id),column)
    return column

def remove_column_from_cache(column_id):
    cache.delete(column_key(column_id))

def get_issue_from_cache(issue_id):
    issue = cache.get(issue_key(issue_id))
    if not issue:
        try:
            issue = Issue.objects.get(id=issue_id)
        except:
            return None
        cache.set(issue_key(issue_id),issue)
    return issue

def remove_issue_from_cache(issue_id):
    cache.delete(issue_key(issue_id))