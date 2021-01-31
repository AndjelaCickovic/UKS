from django.shortcuts import render
from django.http import HttpResponse
from wiki_app.models import Wiki, Page
from wiki_app.forms import PageForm

# Create your views here.

def main(request):
    pages = Page.objects.order_by('id')
    obj_dict = {'pages':pages}

    return render(request,'wiki_app/no_page.html',obj_dict)

def page(request,page_id):
    pages = Page.objects.order_by('id')
    try:
        page = Page.objects.get(id=page_id)
    except:
        return render(request, 'wiki_app/error.html' ,{'pages':pages})
    obj_dict = {'page':page, 'pages':pages}

    return render(request,'wiki_app/page.html',obj_dict)

def new_page(request):
    pages = Page.objects.order_by('id')
    form = PageForm()

    if request.method =='POST' :
        form = PageForm(request.POST)

        if form.is_valid(): 
            page = Page()
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']
            wiki = Wiki.objects.get(id=1)
            page.wiki = wiki
            page.save()

            return render(request,wiki_app/no_page.html,{'pages':pages})
            
    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages})

def edit_page(request, page_id):
    pages = Page.objects.order_by('id')
    try:
        page = Page.objects.get(id=page_id)
    except:
        return render(request, 'wiki_app/error.html' ,{'pages':pages})
    form = PageForm(instance=page)

    if request.method =='POST' :
        form = PageForm(request.POST)

        if form.is_valid(): 
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']

            page.save()

            return render(request, 'wiki_app/no_page.html' ,{'pages':pages})
            
    return render(request,'wiki_app/edit_page.html',{'form':form, 'pages': pages})

def delete_page(request, page_id):
    pages = Page.objects.order_by('id')
    try:
        page = Page.objects.get(id=page_id)
    except:
        return render(request, 'wiki_app/error.html' ,{'pages':pages})

    page.delete()

    return render(request, 'wiki_app/no_page.html' ,{'pages':pages})