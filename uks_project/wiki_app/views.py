from django.shortcuts import render
from django.http import HttpResponse
from wiki_app.models import Wiki, Page

# Create your views here.

def main(request):
    pages = Page.objects.order_by('id')
    obj_dict = {'pages':pages}

    return render(request,'wiki_app/no_page.html',obj_dict)

def page(request,page_id):
    pages = Page.objects.order_by('id')
    page = Page.objects.get(id=page_id)
    obj_dict = {'page':page, 'pages':pages}

    return render(request,'wiki_app/page.html',obj_dict)