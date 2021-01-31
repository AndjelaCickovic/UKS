from django.shortcuts import render
from branches_app.models import Branch

# Create your views here.
def main(request):
    branches = Branch.objects.order_by('id')
    obj_dict = {'branches':branches}

    return render(request,'branches_app/no_branch.html',obj_dict)

def branch(request, branch_id):
    branches = Branch.objects.order_by('id')
    try:
        branch = Branch.objects.get(id=branch_id)
    except:
        print('error')
    
    obj_dict = {
        'branches': branches,
        'branch': branch
    }

    print(branch.parent_branch)

    return render(request,'branches_app/branch.html',obj_dict)