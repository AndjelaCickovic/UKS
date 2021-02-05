from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki_app.models import Wiki, Page
from wiki_app.forms import PageForm
from repositories_app.models import Repository

# Create your views here.

def main(request, repository_id):
    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    obj_dict = {'pages':pages, 'repository': repository}

    return render(request,'wiki_app/no_page.html',obj_dict)

def error(request, repository_id):
    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    obj_dict = {'pages':pages, 'repository': repository}

    return render(request,'wiki_app/error.html',obj_dict)

def page(request,page_id, repository_id):
    try:
        page = Page.objects.get(id=page_id)
    except:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')
    
    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    obj_dict = {'page':page, 'pages':pages, 'repository': repository}

    return render(request,'wiki_app/page.html',obj_dict)

def new_page(request, repository_id):
    repository = Repository.objects.get(id=repository_id)
    form = PageForm()

    if request.method =='POST' :
        form = PageForm(request.POST)

        if form.is_valid(): 
            page = Page()
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']
            page.wiki = repository.wiki.all()[0]
            page.save()

            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repository})

def edit_page(request, page_id, repository_id):
    try:
        page = Page.objects.get(id=page_id)
    except:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')
    form = PageForm(instance=page)

    if request.method =='POST' :
        form = PageForm(request.POST)

        if form.is_valid(): 
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']

            page.save()
            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repository})

def delete_page(request, page_id, repository_id):
    try:
        page = Page.objects.get(id=page_id)
    except:
        repository = Repository.objects.get(id=repository_id)
        pages = repository.wiki.all()[0].pages.all()

        return render(request, 'wiki_app/error.html' ,{'pages':pages, 'repository': repository})

    page.delete()

    return redirect('/repositories/repository/' + str(repository_id) + '/wiki')