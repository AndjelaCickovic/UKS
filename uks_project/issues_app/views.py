from django.shortcuts import render
from django.http import HttpResponse
from issues_app.models import Issue
from issues_app.serializers import IssueSerializer
import sys
import io

# Create your views here.
def main(request):
    issues = Issue.objects.all()
    serializer = IssueSerializer(issues, many=True)
    dictionary = {'issues': serializer.data}
    return render(request, 'issues_app/main.html', context=dictionary)