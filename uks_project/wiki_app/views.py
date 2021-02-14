from django.shortcuts import render, redirect
from django.http import HttpResponse
from wiki_app.models import Wiki, Page
from wiki_app.forms import PageForm
from repositories_app.models import Repository, RepositoryUser
from users.models import AppUser
from django.contrib.auth.decorators import login_required

# Create your views here.

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
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')
    
    role = check_role(request, repository)
    print(role)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    pages = repository.wiki.all()[0].pages.all()

    obj_dict = {'pages':pages, 'repository': repository, 'role': role}

    return render(request,'wiki_app/no_page.html',obj_dict)

def error(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')
    
    role = check_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    pages = repository.wiki.all()[0].pages.all()

    obj_dict = {'pages':pages, 'repository': repository, 'role': role}

    return render(request,'wiki_app/error.html',obj_dict)

def page(request,page_id, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')
    
    role = check_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories')

    pages = repository.wiki.all()[0].pages.all()

    try:
        page = Page.objects.get(id=page_id)
    except:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')

    obj_dict = {'page':page, 'pages':pages, 'repository': repository, 'role': role}

    return render(request,'wiki_app/page.html',obj_dict)

@login_required
def new_page(request, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
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

            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    repository = Repository.objects.get(id=repository_id)
    pages = repository.wiki.all()[0].pages.all()

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repository, 'role': role})

@login_required
def edit_page(request, page_id, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')
    
    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories') 
    elif role == False:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki')

    try:
        page = Page.objects.get(id=page_id)
    except:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')
    form = PageForm(instance=page, initial={'wiki':repository.wiki.all()[0]})

    if request.method =='POST' :
        form = PageForm(request.POST, instance=page)

        if form.is_valid(): 
            page.title = form.cleaned_data['title']
            page.content = form.cleaned_data['content']
            page.message = form.cleaned_data['message']

            page.save()
            return redirect('/repositories/repository/' + str(repository_id) + '/wiki/page/' + str(page.id))

    pages = repository.wiki.all()[0].pages.all()

    return render(request,'wiki_app/new_page.html',{'form':form, 'pages': pages, 'repository': repository, 'role': role})

@login_required
def delete_page(request, page_id, repository_id):
    try:
        repository = Repository.objects.get(id=repository_id)
    except:
        return redirect('/repositories')
    
    role = get_role(request, repository)

    if repository.is_public == False and role == False:
        return redirect('/repositories') 
    elif role == False:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki')

    try:
        page = Page.objects.get(id=page_id)
    except:
        return redirect('/repositories/repository/' + str(repository_id) + '/wiki/error')

    page.delete()

    return redirect('/repositories/repository/' + str(repository_id) + '/wiki')