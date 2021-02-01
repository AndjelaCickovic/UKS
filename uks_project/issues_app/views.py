from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from issues_app.models import Issue, Label, Milestone
from issues_app.serializers import IssueSerializer
from issues_app.forms import LabelForm, MilestoneForm
import sys
import io

# Create your views here.
def main(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    dictionary = {'issues': serializer.data}
    return render(request, 'issues_app/issues.html', context=dictionary)

def labels(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    labels = Label.objects.all()
    dictionary = {'issues': serializer.data, 'labels': labels}
    return render(request, 'issues_app/labels.html', context=dictionary)

def add_label(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    form = LabelForm()

    if request.method =='POST' :
        form = LabelForm(request.POST)

        if form.is_valid(): 
            label = Label()
            label.name = form.cleaned_data['name']
            label.description = form.cleaned_data['description']
            label.colour = form.cleaned_data['colour']
            label.save()
            
            return HttpResponseRedirect(reverse('view_labels'))
            
    dictionary = {'issues': serializer.data, 'form': form}
    return render(request, 'issues_app/new_label.html', context=dictionary)

def delete_label(request, label_id):
    Label.objects.filter(id=label_id).delete()

    return HttpResponseRedirect(reverse('view_labels'))

def edit_label(request, label_id):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    label = Label.objects.get(id=label_id)
    form = LabelForm(initial = {'name': label.name, 'description': label.description, 'colour': label.colour})

    if request.method =='POST' :
        form = LabelForm(request.POST)

        if form.is_valid(): 
            label.name = form.cleaned_data['name']
            label.description = form.cleaned_data['description']
            label.colour = form.cleaned_data['colour']
            label.save()
            
            return HttpResponseRedirect(reverse('view_labels'))
            
    dictionary = {'issues': serializer.data, 'form': form}
    return render(request, 'issues_app/edit_label.html', context=dictionary)

def milestones(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    milestones = Milestone.objects.all()
    dictionary = {'issues': serializer.data, 'milestones': milestones}
    return render(request, 'issues_app/milestones.html', context=dictionary)

def add_milestone(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    form = MilestoneForm()

    if request.method =='POST' :
        form = MilestoneForm(request.POST)

        if form.is_valid(): 
            milestone = Milestone()
            milestone.name = form.cleaned_data['name']
            milestone.dueDate = form.cleaned_data['dueDate']
            milestone.description = form.cleaned_data['description']
            milestone.status = form.cleaned_data['status']
            milestone.save()
            
            return HttpResponseRedirect(reverse('view_milestones'))
            
    dictionary = {'issues': serializer.data, 'form': form}
    return render(request, 'issues_app/new_milestone.html', context=dictionary)

def delete_milestone(request, milestone_id):
    Milestone.objects.filter(id=milestone_id).delete()

    return HttpResponseRedirect(reverse('view_milestones'))

def edit_milestone(request, milestone_id):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
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
            
            return HttpResponseRedirect(reverse('view_milestones'))
            
    dictionary = {'issues': serializer.data, 'form': form}
    return render(request, 'issues_app/edit_milestone.html', context=dictionary)

def change_status_milestone(request, milestone_id):
    milestone = Milestone.objects.get(id=milestone_id)
    if milestone.status == 'Open':
        milestone.status = 'Closed'
    else:
        milestone.status = 'Open'
    milestone.save()

    return HttpResponseRedirect(reverse('view_milestones'))

def issue(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    serializer = IssueSerializer(issue)
    dictionary = {'issue': serializer.data, 'assignees': serializer.data['assignees']}
    print(serializer.data['assignees'])
    return render(request, 'issues_app/issue.html', context=dictionary)

