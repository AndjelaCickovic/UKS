from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki_app.models import Wiki, Page
from wiki_app.forms import PageForm
from repositories_app.models import Repository, RepositoryUser
from users.models import AppUser
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


def pages_key(repository_id):
    return "pages.all."+str(repository_id)

def page_key(page_id):
    return "page."+str(page_id)

def repository_key(id):
    return "repository."+str(id)


def get_role(request, repository):
    try:
        app_user = AppUser.objects.get(user=request.user)
        repository_user = RepositoryUser.objects.get(user=app_user, repository=repository)
        return True
    except:
        return False

def check_role(request, repository):
    if request.user.is_authenticated:
        return get_role(request,repository)
    else:
        return False

def main(request, repository_id):  
    repository = get_repository_from_cache(repository_id)

    if not repository:
        return redirect('/repositories')
    
    role = check_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    pages = get_pages_from_cache(repository)

    obj_dict = {'pages':pages, 'repository': repository, 'role': role}

    return render(request,'wiki_app/no_page.html',obj_dict)

def error(request, repository_id):
    repository = get_repository_from_cache(repository_id)

    if not repository:
        return redirect('/repositories')
    
    role = check_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    pages = get_pages_from_cache(repository)

    obj_dict = {'pages':pages, 'repository': repository, 'role': role}

    return render(request,'wiki_app/error.html',obj_dict)

def page(request,page_id, repository_id):
    repository = get_repository_from_cache(repository_id)

    if not repository:
        return redirect('/repositories')
    
    role = check_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    pages = get_pages_from_cache(repository)

    page = get_page_from_cache(page_id)
    if not page:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')

    obj_dict = {'page':page, 'pages':pages, 'repository': repository, 'role': role}

    return render(request,'wiki_app/page.html',obj_dict)

@login_required
def new_page(request, repository_id):
    repository = get_repository_from_cache(repository_id)

    if not repository:
        return redirect('/repositories')
    
    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories') 
    elif role == False:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki')

    form = PageForm(initial={'wiki':repository.wiki.all()[0]})

    if request.method =='POST' :
        form = PageForm(request.POST)

        if form.is_valid(): 
            page = Page()
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']
            page.wiki = repository.wiki.all()[0]
            page.save()

            remove_repository_from_cache(repository_id)
            remove_pages_from_cache(repository_id)

            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repository, 'role': role})

@login_required
def edit_page(request, page_id, repository_id):
    repository = get_repository_from_cache(repository_id)

    if not repository:
        return redirect('/repositories')
    
    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories') 
    elif role == False:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki')

    page = get_page_from_cache(page_id)
    if not page:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')

    form = PageForm(instance=page, initial={'wiki':repository.wiki.all()[0]})

    if request.method =='POST' :
        form = PageForm(request.POST, instance=page)

        if form.is_valid(): 
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']

            page.save()

            remove_pages_from_cache(repository_id)
            remove_repository_from_cache(repository_id)
            remove_page_from_cache(page_id)
            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    pages = repository.wiki.all()[0].pages.all()

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repository, 'role': role})

@login_required
def delete_page(request, page_id, repository_id):
    repository = get_repository_from_cache(repository_id)

    if not repository:
        return redirect('/repositories')
    
    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories') 
    elif role == False:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki')

    page = get_page_from_cache(page_id)
    if not page:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')

    page.delete()

    remove_pages_from_cache(repository_id)
    remove_repository_from_cache(repository_id)
    remove_page_from_cache(page_id)

    return redirect('/repositories/repository/' + str(repository_id) + '/wiki')

def get_repository_from_cache(repository_id):
    repository = cache.get(repository_key(repository_id))
    if not repository:
        try:
            repository = Repository.objects.get(id=repository_id)
        except:
            return None
        cache.set(repository_key(repository_id),repository)
    return repository

def get_pages_from_cache(repository):
    pages = cache.get(pages_key(repository.id))
    if not pages:
        try:
            pages = Wiki.objects.filter(repository=repository)[0].pages.all()
        except:
            return None
        cache.set(pages_key(repository.id),pages)
    return pages

def get_page_from_cache(page_id):
    page = cache.get(page_key(page_id))
    if not page:
        try:
            page = Page.objects.get(id=page_id)
        except:
            return None
        cache.set(page_key(page_id),page)
    return page

def remove_repository_from_cache(repository_id):
    cache.delete(repository_key(repository_id))

def remove_page_from_cache(page_id):
    cache.delete(page_key(page_id))

def remove_pages_from_cache(repository_id):
    cache.delete(pages_key(repository_id))