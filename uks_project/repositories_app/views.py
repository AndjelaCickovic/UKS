from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from repositories_app.models import Repository, RepositoryUser
from repositories_app.serializers import RepositorySerializer
from django.urls import reverse
from repositories_app.forms import RepositoryForm
from branches_app.models import Branch
from django.contrib.auth.decorators import login_required
from users.models import AppUser
from wiki_app.models import Wiki

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
    return render(request, 'repositories_app/repository.html', context = dictionary)

@login_required
def add_repository(request):
    repositories = Repository.objects.all()
    serializer = RepositorySerializer(repositories, many=True)
    form = RepositoryForm()

    if request.method =='POST' :
        form = RepositoryForm(request.POST)

        if form.is_valid(): 
            repository = Repository()
            repository.name = form.cleaned_data['name']
            repository.description = form.cleaned_data['description']
            repository.is_public = form.cleaned_data['is_public']
            repository.save()
            
            branch = Branch()
            branch.name = 'main'
            #branch.parent_branch = null
            branch.save()

            repository.branches.set([branch])
            repository.save()

            repository_user = RepositoryUser()
            repository_user.user = request.user
            repository_user.role = 'Owner'
            repository_user.save()

            repository.repository_users.set([repository_user])
            repository.save()

            wiki = Wiki()
            wiki.title = repository.name + ' Wiki'
            wiki.save()

            repository.wiki = wiki
            repository.save()


            return HttpResponseRedirect(reverse('repositories_app:view_repositories'))
            
    dictionary = {'repositories': serializer.data, 'form': form}
    return render(request, 'repositories_app/new_repository.html', context=dictionary)

@login_required
def edit_repository(request, repository_id):
    #repositories = Repository.objects.all()
    #serializer = RepositorySerializer(repositories, many=True)
    repository = Repository.objects.get(id=repository_id)
    form = RepositoryForm(initial = {'name': repository.name, 'description': repository.description, 'is_public': repository.is_public})

    if request.method =='POST' :
        form = RepositoryForm(request.POST)

        if form.is_valid(): 
            repository.name = form.cleaned_data['name']
            repository.description = form.cleaned_data['description']
            repository.is_public = form.cleaned_data['is_public']
            repository.save()
            
            return HttpResponseRedirect(reverse('repositories_app:view_repository', args = [repository_id]))
            
    dictionary = {'form': form}
    return render(request, 'repositories_app/edit_repository.html', context=dictionary)