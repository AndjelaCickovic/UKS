from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from issues_app.models import Issue, Label, Milestone
from issues_app.serializers import IssueSerializer, LabelSerializer, MilestoneSerializer
from issues_app.forms import LabelForm, MilestoneForm, IssueForm
from users.models import AppUser
from repositories_app.models import Repository
from repositories_app.serializers import RepositorySerializer
import sys
import io

# Create your views here.
def main(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    dictionary = {'issues': issue_serializer.data, 'repository': repo_serializer.data}
    return render(request, 'issues_app/issues.html', context=dictionary)

def labels(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    labels = Label.objects.filter(repository = repository)
    label_serializer = LabelSerializer(labels, many=True)

    dictionary = {'issues': issue_serializer.data, 'labels': label_serializer.data, 'repository': repo_serializer.data}
    return render(request, 'issues_app/labels.html', context=dictionary)

def add_label(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    form = LabelForm()

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
            
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data}
    return render(request, 'issues_app/new_label.html', context=dictionary)

def delete_label(request, repository_id, label_id):
    Label.objects.filter(id=label_id).delete()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))

def edit_label(request, repository_id, label_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)

    label = Label.objects.get(id=label_id)
    form = LabelForm(initial = {'name': label.name, 'description': label.description, 'colour': label.colour})

    if request.method =='POST' :
        form = LabelForm(request.POST)

        if form.is_valid(): 
            label.name = form.cleaned_data['name']
            label.description = form.cleaned_data['description']
            label.colour = form.cleaned_data['colour']
            label.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))
            
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data}
    return render(request, 'issues_app/edit_label.html', context=dictionary)

def milestones(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    milestones = Milestone.objects.filter(repository = repository)
    milestone_serializer = MilestoneSerializer(milestones, many=True)

    dictionary = {'issues': issue_serializer.data, 'milestones': milestone_serializer.data, 'repository': repo_serializer.data}
    return render(request, 'issues_app/milestones.html', context=dictionary)

def add_milestone(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    form = MilestoneForm()

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
            
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data}
    return render(request, 'issues_app/new_milestone.html', context=dictionary)

def delete_milestone(request, repository_id, milestone_id):
    Milestone.objects.filter(id=milestone_id).delete()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

def edit_milestone(request, repository_id, milestone_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    milestone = Milestone.objects.get(id=milestone_id)
    form = MilestoneForm(initial = {'name': milestone.name, 'description': milestone.description, 'dueDate': milestone.dueDate, 'status': milestone.status})

    if request.method =='POST' :
        form = MilestoneForm(request.POST)

        if form.is_valid():
            milestone.name = form.cleaned_data['name']
            milestone.dueDate = form.cleaned_data['dueDate']
            milestone.description = form.cleaned_data['description']
            milestone.status = form.cleaned_data['status']
            milestone.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))
            
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data}
    return render(request, 'issues_app/edit_milestone.html', context=dictionary)

def change_status_milestone(request, repository_id, milestone_id):
    milestone = Milestone.objects.get(id=milestone_id)
    if milestone.status == 'Open':
        milestone.status = 'Closed'
    else:
        milestone.status = 'Open'
    milestone.save()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

def issue(request, repository_id, issue_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)

    issue = Issue.objects.get(id=issue_id)
    serializer = IssueSerializer(issue)
    assignees = []
    for user in serializer.data['assignees']:
        user = AppUser.objects.get(id=user['id'])
        assignees.append(user)

    dictionary = {'issue': serializer.data, 'assignees': assignees, 'repository': repo_serializer.data}
    return render(request, 'issues_app/issue.html', context=dictionary)

def add_issue(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    issues = Issue.objects.filter(repository = repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    form = IssueForm()

    if request.method =='POST' :
        form = IssueForm(request.POST)

        if form.is_valid(): 
            issue = Issue()
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.save()
            issue.labels.set(form.cleaned_data['labels'])
            issue.assignees.set(form.cleaned_data['assignees'])
            issue.repository = repository
            issue.save()
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))
            
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data}
    return render(request, 'issues_app/new_issue.html', context=dictionary)

def edit_issue(request, repository_id, issue_id):
    print('Start edit method')
    repository = Repository.objects.get(id = repository_id)
    repo_serializer = RepositorySerializer(repository)
    
    issue = Issue.objects.get(id=issue_id)
    serializer = IssueSerializer(issue)
    assignees = []
    for user in serializer.data['assignees']:
        user = AppUser.objects.get(id=user['id'])
        assignees.append(user)
    form = IssueForm(initial = {'name': issue.name, 'comment': issue.comment, 'status': issue.status, 'column': issue.column, 'milestone': issue.milestone, 'assignees': [user for user in issue.assignees.values_list('id', flat=True)], 'labels': [label for label in issue.labels.values_list('id', flat=True)]})

    if request.method =='POST' :
        form = IssueForm(request.POST)

        if form.is_valid():
            issue.name = form.cleaned_data['name']
            issue.comment = form.cleaned_data['comment']
            issue.status = form.cleaned_data['status']
            issue.labels.set(form.cleaned_data['labels'])
            issue.assignees.set(form.cleaned_data['assignees'])
            issue.save()

            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issue', kwargs={'repository_id': repository_id, 'issue_id':issue.id}))
            
    dictionary = {'issue': serializer.data, 'form': form, 'assignees': assignees, 'repository': repo_serializer.data}
    print('Before return')
    return render(request, 'issues_app/edit_issue.html', context=dictionary)

def delete_issue(request, repository_id, issue_id):
    Issue.objects.filter(id=issue_id).delete()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))

def change_status_issue(request, repository_id, issue_id):
    issue = Issue.objects.get(id=issue_id)
    if issue.status == 'Open':
        issue.status = 'Closed'
    else:
        issue.status = 'Open'
    issue.save()

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))

