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
from django.core.cache import cache
import sys
import io

def repository_key(id):
    return "repository."+str(id)

def issues_key(repository_id):
    return "issues.all."+str(repository_id)

def issue_key(issue_id):
    return "issue."+str(issue_id)

def labels_key(repository_id):
    return "labels.all."+str(repository_id)

def label_key(label_id):
    return "label."+str(label_id)

def milestones_key(repository_id):
    return "milestones.all."+str(repository_id)

def milestone_key(milestone_id):
    return "milestone."+str(milestone_id)

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
    
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)
    
    issues = get_issues_from_cache(repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    valid_user = check_if_valid_user(request, repository)
    
    if not repository.is_public and not valid_user:
        return redirect('/repositories')

    dictionary = {'issues': issue_serializer.data, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/issues.html', context=dictionary)

def labels(request, repository_id):

    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
    issue_serializer = IssueSerializer(issues, many=True)
    labels = get_labels_from_cache(repository)
    label_serializer = LabelSerializer(labels, many=True)

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'test_labels': labels, 'labels': label_serializer.data, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/labels.html', context=dictionary)

@login_required
def add_label(request, repository_id):

    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
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
            
            remove_labels_from_cache(repository_id)
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/new_label.html', context=dictionary)

@login_required
def delete_label(request, repository_id, label_id):
    label = get_label_from_cache(label_id)
    
    if not label:
        return redirect('/repositories')

    label.delete()
    remove_label_from_cache(label_id)
    remove_labels_from_cache(repository_id)
    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))

@login_required
def edit_label(request, repository_id, label_id):
   
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
    issue_serializer = IssueSerializer(issues, many=True)

    label = get_label_from_cache(label_id)
    form = LabelForm(initial = {'name': label.name, 'description': label.description, 'colour': label.colour, 'repository': repository})

    if request.method =='POST' :
        form = LabelForm(request.POST, instance=label)

        if form.is_valid(): 
            label.name = form.cleaned_data['name']
            label.description = form.cleaned_data['description']
            label.colour = form.cleaned_data['colour']
            label.save()
            
            remove_label_from_cache(label_id)
            remove_labels_from_cache(repository_id)
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_labels', kwargs={'repository_id':repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/edit_label.html', context=dictionary)

def milestones(request, repository_id):
    
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
    issue_serializer = IssueSerializer(issues, many=True)

    milestones = get_milestones_from_cache(repository)
    milestone_serializer = MilestoneSerializer(milestones, many=True)

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'test_milestones': milestones, 'milestones': milestone_serializer.data, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/milestones.html', context=dictionary)

@login_required
def add_milestone(request, repository_id):
    
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
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

            remove_milestones_from_cache(repository_id)
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/new_milestone.html', context=dictionary)

@login_required
def delete_milestone(request, repository_id, milestone_id):
    milestone = get_milestone_from_cache(milestone_id)

    if not milestone:
        return redirect('/repositories')
        
    milestone.delete()
    remove_milestones_from_cache(repository_id)
    remove_milestone_from_cache(milestone_id)

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

@login_required
def edit_milestone(request, repository_id, milestone_id):
    
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
    issue_serializer = IssueSerializer(issues, many=True)
    
    milestone = get_milestone_from_cache(milestone_id)
    form = MilestoneForm(initial = {'name': milestone.name, 'description': milestone.description, 'dueDate': milestone.dueDate, 'status': milestone.status, 'repository': repository})

    if request.method =='POST' :
        form = MilestoneForm(request.POST, instance=milestone)

        if form.is_valid():
            milestone.name = form.cleaned_data['name']
            milestone.dueDate = form.cleaned_data['dueDate']
            milestone.description = form.cleaned_data['description']
            milestone.status = form.cleaned_data['status']
            milestone.save()
            
            remove_milestone_from_cache(milestone_id)
            remove_milestones_from_cache(repository_id)

            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

    valid_user = check_if_valid_user(request, repository) 
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/edit_milestone.html', context=dictionary)

@login_required
def change_status_milestone(request, repository_id, milestone_id):
    
    milestone = get_milestone_from_cache(milestone_id)

    if milestone.status == 'Open':
        milestone.status = 'Closed'
    else:
        milestone.status = 'Open'

    milestone.save()
    remove_milestone_from_cache(milestone_id)
    remove_milestones_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_milestones', kwargs={'repository_id':repository_id}))

def issue(request, repository_id, issue_id):
    
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)
    issue = get_issue_from_cache(issue_id)
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
    
    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)

    issues = get_issues_from_cache(repository)
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
                assignees.append(user.id)
            issue.assignees.set(assignees)
            issue.repository = repository
            issue.save()

            remove_issues_from_cache(repository_id)
            
            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issues': issue_serializer.data, 'form': form, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/new_issue.html', context=dictionary)

@login_required
def edit_issue(request, repository_id, issue_id):

    repository = get_repository_from_cache(repository_id)
        
    if not repository:
        return redirect('/repositories')

    repo_serializer = RepositorySerializer(repository)
        
    issue = get_issue_from_cache(issue_id)
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
                choosen_assignees.append(user.id)
            issue.assignees.set(choosen_assignees)
            issue.save()

            remove_issues_from_cache(repository_id)
            remove_issue_from_cache(issue_id)

            return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id': repository_id}))
            
    valid_user = check_if_valid_user(request, repository)
    dictionary = {'issue': serializer.data, 'form': form, 'assignees': assignees, 'repository': repo_serializer.data, 'in_repo': valid_user}
    return render(request, 'issues_app/edit_issue.html', context=dictionary)

@login_required
def delete_issue(request, repository_id, issue_id):
    
    issue = get_issue_from_cache(issue_id)
    if not issue:
        return redirect('/repositories')

    issue.delete()
    remove_issue_from_cache(issue_id)
    remove_issues_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))

@login_required
def change_status_issue(request, repository_id, issue_id):

    issue = get_issue_from_cache(issue_id)
    if issue.status == 'Open':
        issue.status = 'Closed'
    else:
        issue.status = 'Open'
    issue.save()
    remove_issue_from_cache(issue_id)
    remove_issues_from_cache(repository_id)

    return HttpResponseRedirect(reverse('repositories_app:issues_app:view_issues', kwargs={'repository_id':repository_id}))

def get_repository_from_cache(repository_id):
    repository = cache.get(repository_key(repository_id))
    if not repository:
        try:
            repository = Repository.objects.get(id=repository_id)
        except:
            return None
        cache.set(repository_key(repository_id),repository)
    return repository

def get_issues_from_cache(repository):
    issues = cache.get(issues_key(repository.id))
    
    if not issues:
        issues = Issue.objects.filter(repository = repository)
        cache.set(issues_key(repository.id),issues)

    return issues

def get_issue_from_cache(issue_id):

    issue = cache.get(issue_key(issue_id))

    if not issue:
        issue = Issue.objects.get(id=issue_id)
        cache.set(issue_key(issue_id),issue)
    return issue

def get_labels_from_cache(repository):
    labels = cache.get(labels_key(repository.id))
    
    if not labels:
        labels = Label.objects.filter(repository = repository)
        cache.set(labels_key(repository.id),labels)

    return labels

def get_label_from_cache(label_id):

    label = cache.get(label_key(label_id))

    if not label:
        try:
            label = Label.objects.get(id=label_id)
        except:
            return None
        cache.set(label_key(label_id),label)
    return label

def get_milestones_from_cache(repository):
    milestones = cache.get(milestones_key(repository.id))
    
    if not milestones:
        milestones = Milestone.objects.filter(repository = repository)
        cache.set(milestones_key(repository.id),milestones)

    return milestones

def get_milestone_from_cache(milestone_id):
    milestone = cache.get(milestone_key(milestone_id))

    if not milestone:
        try:
            milestone = Milestone.objects.get(id=milestone_id)
        except:
            return None
        cache.set(milestone_key(milestone_id),milestone)
    return milestone

def remove_repository_from_cache(repository_id):
    cache.delete(repository_key(repository_id))

def remove_issues_from_cache(repository_id):
    cache.delete(issues_key(repository_id))

def remove_issue_from_cache(issue_id):
    cache.delete(issue_key(issue_id))

def remove_labels_from_cache(repository_id):
    cache.delete(labels_key(repository_id))

def remove_label_from_cache(label_id):
    cache.delete(label_key(label_id))

def remove_milestones_from_cache(repository_id):
    cache.delete(milestones_key(repository_id))

def remove_milestone_from_cache(milestone_id):
    cache.delete(milestone_key(milestone_id))

