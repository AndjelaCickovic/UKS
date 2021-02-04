from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki_app.models import Wiki, Page
from wiki_app.forms import PageForm
from repositories_app.models import Repository
from repositories_app.serializers import RepositorySerializer

# Create your views here.

def main(request, repository_id):
    pages = Page.objects.order_by('id')
    repository = Repository.objects.get(id=repository_id)
    repo = RepositorySerializer(repository)

    obj_dict = {'pages':pages, 'repository': repo.data}

    return render(request,'wiki_app/no_page.html',obj_dict)

def error(request, repository_id):
    pages = Page.objects.order_by('id')
    repository = Repository.objects.get(id=repository_id)
    repo = RepositorySerializer(repository)

    obj_dict = {'pages':pages, 'repository': repo.data}

    return render(request,'wiki_app/error.html',obj_dict)

def page(request,page_id, repository_id):
    pages = Page.objects.order_by('id')
    try:
        page = Page.objects.get(id=page_id)
    except:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')
    
    repository = Repository.objects.get(id=repository_id)
    repo = RepositorySerializer(repository)

    obj_dict = {'page':page, 'pages':pages, 'repository': repo.data}

    return render(request,'wiki_app/page.html',obj_dict)

def new_page(request, repository_id):
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

            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    repository = Repository.objects.get(id=repository_id)
    repo = RepositorySerializer(repository)

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repo.data})

def edit_page(request, page_id, repository_id):
    pages = Page.objects.order_by('id')
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
    repo = RepositorySerializer(repository)

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repo.data})

def delete_page(request, page_id, repository_id):
    pages = Page.objects.order_by('id')
    try:
        page = Page.objects.get(id=page_id)
    except:
        repository = Repository.objects.get(id=repository_id)
        repo = RepositorySerializer(repository)

        return render(request, 'wiki_app/error.html' ,{'pages':pages, 'repository': repo.data})

    page.delete()

    return redirect('/repositories/repository/' + str(repository_id) + '/wiki')