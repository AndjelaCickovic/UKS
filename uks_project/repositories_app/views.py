from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from repositories_app.models import Repository
from repositories_app.serializers import RepositorySerializer
from django.urls import reverse

# Create your views here.
def main(request):
    repositories = Repository.objects.all()
    serializer = RepositorySerializer(repositories, many=True)
    dictionary = {'repositories': serializer.data}
    return render(request, 'repositories_app/repositories.html', context = dictionary)

def repository(request, repository_id):
    repository = Repository.objects.get(id = repository_id)
    serializer = RepositorySerializer(repository)
    dictionary = {'repository': serializer.data}
    print(serializer.data)
    return render(request, 'repositories_app/repository.html', context = dictionary)