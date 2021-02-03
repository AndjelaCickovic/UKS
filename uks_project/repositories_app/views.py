from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from repositories_app.models import Repository
from django.urls import reverse

# Create your views here.
def main(request):
    repositories = Repository.objects.all()
    dictionary = {'repositories': repositories}
    return render(request, 'repositories_app/repositories.html', context = dictionary)

def repository(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    dictionary = { 'repository': repository}
    return render(request, 'repositories_app/repository.html', context = dictionary)