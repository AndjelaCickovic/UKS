from django.shortcuts import render
from branches_app.models import Branch

# Create your views here.
def main(request):
    branches = Branch.objects.order_by('id')
    obj_dict = {'branches':branches}

    return render(request,'branches_app/main.html',obj_dict)