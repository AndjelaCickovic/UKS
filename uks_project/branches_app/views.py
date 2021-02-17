from django.shortcuts import render,redirect
from branches_app.models import Branch, Commit
from branches_app.forms import BranchForm,EditBranchForm,CommitForm
from repositories_app.models import Repository,RepositoryUser
from django.contrib.auth.decorators import login_required
from users.models import AppUser 
from django.core.cache import cache


def branches_key(repository_id):
    return "branches.all." + str(repository_id)

def branch_key(id):
    return "branch."+str(id)

def repository_key(id):
    return "repository."+str(id)

# Create your views here.
def main(request, repository_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')
    
    if not repository.is_public and not is_in_role(request.user,repository):
        return redirect('/repositories')

    branches = get_branches_from_cache(repository)

    obj_dict = {'branches':branches,'repository':repository,'can_edit':is_in_role(request.user,repository)}

    return render(request,'branches_app/main.html',obj_dict)

@login_required
def new_branch(request,repository_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    branches = get_branches_from_cache(repository)

    if not repository.is_public and not is_in_role(request.user,repository):
        return redirect('/repositories')

    form = BranchForm(repository_id)

    obj_dict = {
        'title' : 'New branch',
        'form': form,
        'repository':repository,
        'branches':branches,
        'can_edit':is_in_role(request.user,repository)
    }


    if request.method == 'POST':
        form_data = BranchForm(repository_id,request.POST)

        if form_data.is_valid():
            branch = Branch(**form_data.cleaned_data)
            branch.repository = repository

            try:
                branch.save()
            except:
                obj_dict['error_add']='Adding branch failed. Branch with that name already exists.'
                return render(request,'branches_app/new_branch.html',obj_dict)

            remove_branches_from_cache(repository_id)
            return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    return render(request,'branches_app/new_branch.html',obj_dict)

@login_required
def edit_branch(request,repository_id,branch_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    if not repository.is_public and not is_in_role(request.user,repository):
        return redirect('/repositories')

    branches = get_branches_from_cache(repository)

    branch = get_branch_from_cache(branch_id)
    if not branch:
        return redirect('repositories/repository/{}/branches'.format(str(repository_id)))


    form = EditBranchForm(instance=branch)

    obj_dict = {
        'title' : 'Edit branch',
        'form': form,
        'repository':repository,
        'branches':branches,
        'can_edit':is_in_role(request.user,repository)
    }

    if request.method == 'POST':
        form_data = EditBranchForm(request.POST)

        if form_data.is_valid():
            branch.name = form_data.cleaned_data['name']
            try:
                branch.save()
            except:
                obj_dict['error']='Updating branch name failed. Branch with that name already exists.'
                return render(request,'branches_app/new_branch.html',obj_dict)

            remove_branch_from_cache(branch_id)
            remove_branches_from_cache(repository_id)

            return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    return render(request,'branches_app/new_branch.html',obj_dict)

@login_required
def delete_branch(request,repository_id,branch_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    branch = get_branch_from_cache(branch_id)
    if not branch:
        return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    if not repository.is_public and not is_in_role(request.user,repository):
        return redirect('/repositories')

    if branch.default:
        branches = Branch.objects.filter(repository=repository)
        obj_dict = {
            'branches':branches,
            'repository':repository,
            'can_edit':is_in_role(request.user,repository),
            'error':'Unable to delete default branch {}'.format(branch.name)}

        return render(request,'branches_app/main.html',obj_dict)

    branch.delete()
    remove_branch_from_cache(branch_id)
    remove_branches_from_cache(repository_id)
    return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

def commits(request, repository_id, branch_id):
   
    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    if not repository.is_public and not is_in_role(request.user,repository):
        return redirect('/repositories')

    branch = get_branch_from_cache(branch_id)
    if not branch:
        return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    obj_dict = {
        'branch': branch,
        'repository':repository,
        'can_edit':is_in_role(request.user,repository)
    }

    return render(request,'branches_app/commits.html',obj_dict)

@login_required
def new_commit(request,repository_id,branch_id):

    repository = get_repository_from_cache(repository_id)
    if not repository:
        return redirect('/repositories')

    branch = get_branch_from_cache(branch_id)
    if not branch:
        return redirect('repositories/repository/{}/branches'.format(str(repository_id)))

    if not repository.is_public and not is_in_role(request.user,repository):
        return redirect('repositories/repository/{}/branches'.format(str(repository_id)))

    form = CommitForm()

    obj_dict = {
        'title' : 'New commit',
        'form': form,
        'repository':repository,
        'branch':branch,
        'can_edit':is_in_role(request.user,repository)
    }


    if request.method == 'POST':
        form_data = CommitForm(request.POST)

        if form_data.is_valid():
            commit = Commit(**form_data.cleaned_data)
            commit.user = AppUser.objects.get(user=request.user)
            try:
                commit.save()
            except:
                obj_dict['error_add']='Adding commit failed.'
                return render(request,'branches_app/new_commit.html',obj_dict)

            branch.commits.add(commit)

            try:
                branch.save()
            except:
                obj_dict['error_add']='Adding commit to branch {} failed.'.format(branch.name)
                return render(request,'branches_app/new_commit.html',obj_dict)

            remove_branch_from_cache(branch_id)
            remove_branches_from_cache(repository_id)

            return redirect('/repositories/repository/{}/branches/{}/commits'.format(str(repository_id),str(branch_id)))

    return render(request,'branches_app/new_commit.html',obj_dict)

def is_in_role(user, repository):
    if user.is_authenticated:
        try:
            app_user = AppUser.objects.get(user=user)
        except:
            return False
        return RepositoryUser.objects.filter(user=app_user, repository=repository).exists()
    else:
        return False

def get_repository_from_cache(repository_id):
    repository = cache.get(repository_key(repository_id))
    if not repository:
        try:
            repository = Repository.objects.get(id=repository_id)
        except:
            return None
        cache.set(repository_key(repository_id),repository)
    return repository

def get_branches_from_cache(repository):
    branches = cache.get(branches_key(repository.id))
    if not branches:
        branches = Branch.objects.filter(repository=repository)
        cache.set(branches_key(repository.id),branches)
    return branches

def remove_branches_from_cache(repository_id):
    cache.delete(branches_key(repository_id))

def get_branch_from_cache(branch_id):
    branch = cache.get(branch_key(branch_id))
    if not branch:
        try:
            branch = Branch.objects.get(id=branch_id)
        except:
            return None
        cache.set(branch_key(branch_id),branch)
    return branch

def remove_branch_from_cache(branch_id):
    cache.delete(branch_key(branch_id))

