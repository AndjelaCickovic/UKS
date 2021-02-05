from django.shortcuts import render
from branches_app.models import Branch, Commit

# Create your views here.
def main(request, repository_id):
    branches = Branch.objects.order_by('id')
    obj_dict = {'branches':branches}

    return render(request,'branches_app/main.html',obj_dict)

def branch(request, branch_id):
    branches = Branch.objects.order_by('id')
    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        print('error')

    print(branch.commits)

    obj_dict = {
        'branches': branches,
        'branch': branch,
        'commits': branch.commits.all()
    }

    return render(request,'branches_app/branch.html',obj_dict)