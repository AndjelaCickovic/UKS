from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from repositories_app.models import Repository, RepositoryUser
from repositories_app.serializers import RepositorySerializer
from django.urls import reverse
from repositories_app.forms import RepositoryForm, RepositoryUserForm
from branches_app.models import Branch
from django.contrib.auth.decorators import login_required
from users.models import AppUser
from wiki_app.models import Wiki

# Create your views here.
def is_owner_or_coowner(request, repository):
    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)
            repository_user = RepositoryUser.objects.get(user=app_user, repository=repository)
            if repository_user.role == 'Owner' or repository_user.role == 'Coowner':
                return True
            else:
                return False
        except:
            return False
    else:
        return False


def main(request):
    if request.user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=request.user)
            repositories = Repository.objects.filter(members = app_user)
            dictionary = {'repositories': repositories}
            return render(request, 'repositories_app/repositories.html', context = dictionary)
        except:
            return redirect('/')
    else:
        return redirect('/')
   
def repository(request, repository_id):
    try:
        repository = Repository.objects.get(id = repository_id)
    except:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))
    
    is_owner = is_owner_or_coowner(request, repository)

    dictionary = {'repository': repository, 'is_owner' : is_owner }
    return render(request, 'repositories_app/repository.html', context = dictionary)

@login_required
def add_repository(request):
    app_user = AppUser.objects.get(user=request.user)
    repositories = Repository.objects.filter(members = app_user)
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
            branch.repository = repository
            branch.default = True
            branch.save()

            repository_user = RepositoryUser()
            repository_user.user = AppUser.objects.get(user=request.user)
            repository_user.role = 'Owner'
            repository_user.repository = repository
            repository_user.save()

            repository.members.add(AppUser.objects.get(user=request.user))
            repository.save()

            wiki = Wiki()
            wiki.repository = repository
            wiki.save()

            return HttpResponseRedirect(reverse('repositories_app:view_repositories'))
            
    dictionary = {'repositories': repositories, 'form': form}
    return render(request, 'repositories_app/new_repository.html', context=dictionary)

@login_required
def edit_repository(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    is_owner = is_owner_or_coowner(request, repository)

    if is_owner == False:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))
    
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

@login_required
def delete_repository(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    is_owner = is_owner_or_coowner(request, repository)

    if is_owner == False:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    repository.delete()
    return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

@login_required
def delete_member(request, member_id, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    is_owner = is_owner_or_coowner(request, repository)

    if is_owner == False:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    try:
        RepositoryUser.objects.filter(id=member_id).delete()
    except:
        pass
    
    return HttpResponseRedirect(reverse('repositories_app:view_repository',args = [repository_id]))

@login_required
def add_member(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    is_owner = is_owner_or_coowner(request, repository)

    if is_owner == False:
        return HttpResponseRedirect(reverse('repositories_app:view_repositories'))

    serializer = RepositorySerializer(repository)
    existing_members = serializer.data['members']
    form = RepositoryUserForm(my_arg = existing_members)

    if request.method =='POST' :
        form = RepositoryUserForm(request.POST, my_arg = existing_members)

        if form.is_valid(): 
            repository_user = RepositoryUser()
            repository_user.user = form.cleaned_data['user']
            repository_user.role = form.cleaned_data['role']
            repository_user.repository = repository
            repository_user.save()

            repository.members.add(repository_user.user)
            repository.save()

            return HttpResponseRedirect(reverse('repositories_app:view_repository', args = [repository_id]))
            
    dictionary = {'repository': repository, 'form': form, 'is_owner' : is_owner}
    return render(request, 'repositories_app/new_member.html', context=dictionary)
