from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from issues_app.models import Issue, Label, Milestone
from issues_app.serializers import IssueSerializer, LabelSerializer, MilestoneSerializer
from issues_app.forms import LabelForm, MilestoneForm, IssueForm
from users.models import AppUser
from repositories_app.models import Repository, RepositoryUser
from repositories_app.serializers import RepositorySerializer
from django.contrib.auth.decorators import login_required
import sys
import io

def check_if_in_repository(request, repository):
    try:
        app_user = AppUser.objects.get(user = request.user)
        repository_user = RepositoryUser.objects.get(user = app_user, repository = repository)
        return True
    except:
        return False

def check_if_app_user(request):
    return request.user.is_authenticated

def check_if_valid_user(request, repository):
    return check_if_app_user(request) and check_if_in_repository(request, repository)

# Create your views here.
def main(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')
    
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/issues.html', context=dictionary)

def labels(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')

    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    labels = Label.objects.filter(repository = repository)
    label_serializer = LabelSerializer(labels, many=True)

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'test_labels': labels, 'labels': label_serializer.data, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/labels.html', context=dictionary)

@login_required
def add_label(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')

    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    form = LabelForm(initial={'repository': repository})

    if request.method =='POST' :
        form = LabelForm(request.POST)

        if form.is_valid(): 
            label = Label()
            label.name = form.cleaned_data['name']
            label.description = form.cleaned_data['description']
            label.colour = form.cleaned_data['colour']
            label.repository = repository
            label.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/new_label.html', context=dictionary)

@login_required
def delete_label(request, repository_id, label_id):
    Label.objects.filter(id=label_id).delete()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))

@login_required
def edit_label(request, repository_id, label_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')

    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)

    label = Label.objects.get(id=label_id)
    form = LabelForm(initial = {'name': label.name, 'description': label.description, 'colour': label.colour, 'repository': repository})

    if request.method =='POST' :
        form = LabelForm(request.POST, instance=label)

        if form.is_valid(): 
            label.name = form.cleaned_data['name']
            label.description = form.cleaned_data['description']
            label.colour = form.cleaned_data['colour']
            label.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/edit_label.html', context=dictionary)

def milestones(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')

    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    milestones = Milestone.objects.filter(repository = repository)
    milestone_serializer = MilestoneSerializer(milestones, many=True)

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'milestones': milestone_serializer.data, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/milestones.html', context=dictionary)

@login_required
def add_milestone(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')

    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    form = MilestoneForm(initial={'repository': repository})

    if request.method =='POST' :
        form = MilestoneForm(request.POST)

        if form.is_valid(): 
            milestone = Milestone()
            milestone.name = form.cleaned_data['name']
            milestone.dueDate = form.cleaned_data['dueDate']
            milestone.description = form.cleaned_data['description']
            milestone.status = form.cleaned_data['status']
            milestone.repository = repository
            milestone.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/new_milestone.html', context=dictionary)

@login_required
def delete_milestone(request, repository_id, milestone_id):
    Milestone.objects.filter(id=milestone_id).delete()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

@login_required
def edit_milestone(request, repository_id, milestone_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')
        
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    milestone = Milestone.objects.get(id=milestone_id)
    form = MilestoneForm(initial = {'name': milestone.name, 'description': milestone.description, 'dueDate': milestone.dueDate, 'status': milestone.status, 'repository': repository})

    if request.method =='POST' :
        form = MilestoneForm(request.POST, instance=milestone)

        if form.is_valid():
            milestone.name = form.cleaned_data['name']
            milestone.dueDate = form.cleaned_data['dueDate']
            milestone.description = form.cleaned_data['description']
            milestone.status = form.cleaned_data['status']
            milestone.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

    valid_user = check_if_valid_user(request, repository) 
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/edit_milestone.html', context=dictionary)

@login_required
def change_status_milestone(request, repository_id, milestone_id):
    milestone = Milestone.objects.get(id=milestone_id)
    if milestone.status == 'Open':
        milestone.status = 'Closed'
    else:
        milestone.status = 'Open'
    milestone.save()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

def issue(request, repository_id, issue_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')

    issue = Issue.objects.get(id=issue_id)
    serializer = IssueSerializer(issue)
    assignees = []
    for user in serializer.data['assignees']:
        user = AppUser.objects.get(id=user['id'])
        assignees.append(user)

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issue': serializer.data, 'assignees': assignees, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/issue.html', context=dictionary)

@login_required
def add_issue(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')
        
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    form = IssueForm(repository = repository)

    if request.method =='POST' :
        form = IssueForm(request.POST, repository = repository)

        if form.is_valid(): 
            issue = Issue()
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.save()
            issue.labels.set(form.cleaned_data['labels'])
            issue.milestone = form.cleaned_data['milestone']
            assignees = []
            for user in form.cleaned_data['assignees']:
                print(user.user)
                assignees.append(user.user)
            issue.assignees.set(assignees)
            issue.repository = repository
            issue.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/new_issue.html', context=dictionary)

@login_required
def edit_issue(request, repository_id, issue_id):
    try:
        repository = Repository.objects.get(id = repository_id)
        repo_serializer = RepositorySerializer(repository)
    except:
        return redirect('/repositories')
        
    issue = Issue.objects.get(id=issue_id)
    serializer = IssueSerializer(issue)
    assignees = []
    for user in serializer.data['assignees']:
        user = AppUser.objects.get(id=user['id'])
        assignees.append(user)
    #form = IssueForm(initial = {'name': issue.name, 'comment': issue.comment, 'status': issue.status, 'column': issue.column, 'milestone': issue.milestone, 'assignees': [user for user in issue.assignees.values_list('id', flat=True)], 'labels': [label for label in issue.labels.values_list('id', flat=True)]})
    form = IssueForm(initial = {'name': issue.name, 'comment': issue.comment, 'status': issue.status, 'column': issue.column, 'milestone': issue.milestone, 'assignees': [user for user in issue.assignees.values_list('id', flat=True)], 'labels': [label for label in issue.labels.values_list('id', flat=True)]}, repository = repository)

    if request.method =='POST' :
        form = IssueForm(request.POST, repository = repository)

        if form.is_valid():
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.labels.set(form.cleaned_data['labels'])
            issue.milestone = form.cleaned_data['milestone']
            choosen_assignees = []
            for user in form.cleaned_data['assignees']:
                choosen_assignees.append(user.user)
            issue.assignees.set(choosen_assignees)
            issue.save()

            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issue', kwargs={'repository_id': repository_id, 'issue_id':issue.id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issue': serializer.data, 'form': form, 'assignees': assignees, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/edit_issue.html', context=dictionary)

@login_required
def delete_issue(request, repository_id, issue_id):
    Issue.objects.filter(id=issue_id).delete()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))

@login_required
def change_status_issue(request, repository_id, issue_id):
    issue = Issue.objects.get(id=issue_id)
    if issue.status == 'Open':
        issue.status = 'Closed'
    else:
        issue.status = 'Open'
    issue.save()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))

