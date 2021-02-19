from django.test import TestCase
from django.urls import reverse
from wiki_app.models import Page, Wiki
from repositories_app.models import Repository, RepositoryUser
from users.models import AppUser
from wiki_app.forms import PageForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def create_repository():
    rep = Repository(id=1,is_public=True,name='test_repository')
    rep.save()
    return rep

def create_wiki():
    return Wiki.objects.create(repository=create_repository())

def create_page(title, desc, message):
    return Page.objects.create(title=title,content=desc,message=message, wiki=create_wiki())

class PagesViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        AppUser.objects.create(user=user)

    def test_no_pages(self):
        create_wiki()
        response = self.client.get(reverse('repositories_app:wiki_app:main',kwargs={'repository_id':1}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual(response.context['pages'],[])

    def test_pages(self):
        page = create_page("test_page","test_page_desc","test_page_msg")
        response = self.client.get(reverse('repositories_app:wiki_app:main',kwargs={'repository_id':1}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual(response.context['pages'],['<Page: Page object (' + str(page.id) + ')>'])

    def test_valid_page_details(self):
        test_page = create_page("test_page","test_page_desc","test_page_msg")
        response = self.client.get(reverse('repositories_app:wiki_app:page',kwargs={'repository_id':1, 'page_id':test_page.id}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual([response.context['page']],['<Page: Page object (' + str(test_page.id) + ')>'])

    def test_invalid_page_details(self):
        response = self.client.get(reverse('repositories_app:wiki_app:page',kwargs={'repository_id':1, 'page_id':5}))
        self.assertEquals(response.status_code,302)

    def test_delete_valid_page(self):
        self.client.login(username='temporary', password='temporary')
        test_page = create_page("test_page","test_page_desc","test_page_msg")
        temp_user = AppUser.objects.get(user=User.objects.get(username='temporary'))
        RepositoryUser.objects.create(user=temp_user, repository=Repository.objects.get(id=1), role='Owner')
        response = self.client.get(reverse('repositories_app:wiki_app:delete',kwargs={'repository_id':1, 'page_id':test_page.id}))
        exists = Page.objects.filter(id=test_page.id).exists()
        self.assertEquals(exists,False)

    def test_delete_invalid_page(self):
        create_repository()
        self.client.login(username='temporary', password='temporary')
        temp_user = AppUser.objects.get(user=User.objects.get(username='temporary'))
        RepositoryUser.objects.create(user=temp_user, repository=Repository.objects.get(id=1), role='Owner')
        response = self.client.get(reverse('repositories_app:wiki_app:delete',kwargs={'repository_id':1, 'page_id':25}))
        self.assertEquals(response.status_code,302)

class PagesFormTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        AppUser.objects.create(user=user)

    def test_new_page_valid_form(self):
        form = PageForm(data={'title':'title','content':'desc','wiki':create_wiki()})
        self.assertTrue(form.is_valid())

    def test_new_page_post_valid_form(self):
        wiki = create_wiki()
        self.client.login(username='temporary', password='temporary')
        temp_user = AppUser.objects.get(user=User.objects.get(username='temporary'))
        RepositoryUser.objects.create(user=temp_user, repository=Repository.objects.get(id=1), role='Owner')
        response  = self.client.post(reverse("repositories_app:wiki_app:new",kwargs={'repository_id':1}),data={'title':'title','content':'desc'})
        self.assertEquals(response.status_code,200)
        self.assertFormError(response,'form','title',None)
        self.assertFormError(response,'form','content',None)

    def test_new_page_post_invalid_form(self):
        wiki = create_wiki()
        self.client.login(username='temporary', password='temporary')
        temp_user = AppUser.objects.get(user=User.objects.get(username='temporary'))
        RepositoryUser.objects.create(user=temp_user, repository=Repository.objects.get(id=1), role='Owner')
        response  = self.client.post(reverse("repositories_app:wiki_app:new",kwargs={'repository_id':1}),data={'title':'','content':'desc'})
        self.assertEquals(response.status_code,200)
        self.assertFormError(response,'form','title','This field is required.')

    def test_edit_post_valid_form(self):
        test_page = create_page("test_page","test_page_desc","test_page_msg")        
        self.client.login(username='temporary', password='temporary')
        temp_user = AppUser.objects.get(user=User.objects.get(username='temporary'))
        RepositoryUser.objects.create(user=temp_user, repository=Repository.objects.get(id=1), role='Owner')
        response  = self.client.post(reverse("repositories_app:wiki_app:edit",kwargs={'repository_id':1, 'page_id':test_page.id}),data={'title':'titile','content':'desc'})
        self.assertFormError(response,'form','title',None)
        self.assertFormError(response,'form','content',None)

    def test_edit_post_invalid_form(self):
        test_page = create_page("test_page","test_page_desc","test_page_msg")        
        self.client.login(username='temporary', password='temporary')
        temp_user = AppUser.objects.get(user=User.objects.get(username='temporary'))
        RepositoryUser.objects.create(user=temp_user, repository=Repository.objects.get(id=1), role='Owner')
        response  = self.client.post(reverse("repositories_app:wiki_app:edit",kwargs={'repository_id':1, 'page_id':test_page.id}),data={'title':'','content':'desc'})
        self.assertFormError(response,'form','title','This field is required.')