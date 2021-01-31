from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from issues_app.models import Issue, Label
from issues_app.serializers import IssueSerializer
from issues_app.forms import LabelForm
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
    labels = Label.objects.all()
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
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    labels = Label.objects.all()

    return HttpResponseRedirect(reverse('view_labels'))

def edit_label(request, label_id):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    labels = Label.objects.all()
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