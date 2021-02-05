from django.shortcuts import render,redirect
from branches_app.models import Branch, Commit
from branches_app.forms import BranchForm
from repositories_app.models import Repository

# Create your views here.
def main(request, repository_id):

    repository = Repository.objects.get(id=repository_id)

    branches = Branch.objects.filter(repository=repository)
    obj_dict = {'branches':branches,'repository':repository}

    return render(request,'branches_app/main.html',obj_dict)

def branch(request, repository_id, branch_id):

    repository = Repository.objects.get(id=repository_id)
    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        print('error')

    obj_dict = {
        'branch': branch,
        'repository':repository
    }

    return render(request,'branches_app/branch.html',obj_dict)

def new_branch(request,repository_id):

    form = BranchForm(repository_id)
    repository = Repository.objects.get(id=repository_id)

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