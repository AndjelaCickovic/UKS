from django.shortcuts import render,redirect
from branches_app.models import Branch, Commit
from branches_app.forms import BranchForm,EditBranchForm
from repositories_app.models import Repository
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def main(request, repository_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    branches = Branch.objects.filter(repository=repository)
    obj_dict = {'branches':branches,'repository':repository}

    return render(request,'branches_app/main.html',obj_dict)

@login_required
def commits(request, repository_id, branch_id):
   
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    obj_dict = {
        'branch': branch,
        'repository':repository
    }

    return render(request,'branches_app/commits.html',obj_dict)

@login_required
def new_branch(request,repository_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    branches = Branch.objects.filter(repository=repository)

    form = BranchForm(repository_id)

    obj_dict = {
        'title' : 'New branch',
        'form': form,
        'repository':repository,
        'branches':branches
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

            return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    return render(request,'branches_app/new_branch.html',obj_dict)

@login_required
def edit_branch(request,repository_id,branch_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    branches = Branch.objects.filter(repository=repository)

    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        return redirect('repositories/repository/{}/branches'.format(str(repository_id)))

    form = EditBranchForm(instance=branch)

    obj_dict = {
        'title' : 'Edit branch',
        'form': form,
        'repository':repository,
        'branches':branches
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

            return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    return render(request,'branches_app/new_branch.html',obj_dict)

@login_required
def delete_branch(request,repository_id,branch_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        return redirect('repositories/repository/{}/branches'.format(str(repository_id)))

    if branch.default:
        branches = Branch.objects.filter(repository=repository)
        obj_dict = {'branches':branches,'repository':repository,'error':'Unable to delete default branch {}'.format(branch.name)}
        return render(request,'branches_app/main.html',obj_dict)

    branch.delete()
    return redirect('repositories/repository/{}/branches'.format(str(repository_id)))