from django.shortcuts import render,redirect
from branches_app.models import Branch, Commit
from branches_app.forms import BranchForm,EditBranchForm
from repositories_app.models import Repository

# Create your views here.
def main(request, repository_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    branches = Branch.objects.filter(repository=repository)
    obj_dict = {'branches':branches,'repository':repository}

    return render(request,'branches_app/main.html',obj_dict)

def branch(request, repository_id, branch_id):
   
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

    return render(request,'branches_app/branch.html',obj_dict)

def new_branch(request,repository_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    form = BranchForm(repository_id)

    obj_dict = {
        'form': form,
        'repository':repository
    }


    if request.method == 'POST':
        form_data = BranchForm(repository_id,request.POST)

        if form_data.is_valid():
            branch = Branch(**form_data.cleaned_data)
            branch.repository = repository
            try:
                branch.save()
            except:
                obj_dict['err']='Adding branch failed. Branch with that name already exists.'
                return render(request,'branches_app/new_branch.html',obj_dict)

            return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    return render(request,'branches_app/new_branch.html',obj_dict)

def edit_branch(request,repository_id,branch_id):

    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')

    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        return redirect('repositories/repository/{}/branches'.format(str(repository_id)))

    form = EditBranchForm(instance=branch)

    obj_dict = {
        'form': form,
        'repository':repository
    }

    if request.method == 'POST':
        form_data = EditBranchForm(request.POST)

        if form_data.is_valid():
            branch.name = form_data.cleaned_data['name']
            try:
                branch.save()
            except:
                obj_dict['err']='Updating branch name failed. Branch with that name already exists.'
                return render(request,'branches_app/new_branch.html',obj_dict)

            return redirect('/repositories/repository/{}/branches'.format(str(repository_id)))

    return render(request,'branches_app/new_branch.html',obj_dict)
