from django.shortcuts import render
from django.http import HttpResponse
from wiki_app.models import Wiki, Page
# Create your views here.

def main(request):
    pages = Page.objects.order_by('id')
    obj_dict = {'pages':pages}

    return render(request,'wiki_app/main.html',obj_dict)