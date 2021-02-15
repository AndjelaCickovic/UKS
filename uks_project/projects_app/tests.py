from django.test import TestCase
from django.urls import reverse
from projects_app.models import Project
from repositories_app.models import Repository
from projects_app.forms import ProjectForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def create_repository():
    rep = Repository(id=1,is_public=True,name='test_repository')
    rep.save()
    return rep

def create_project(name, description, status):
    return Project.objects.create(name=name,description=description,status=status, repository=create_repository())

class ProjectsViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_no_projects(self):
        create_repository()
        response = self.client.get(reverse('repositories_app:projects_app:main',kwargs={'repository_id':1}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual(response.context['projects'],[])

    def test_projects(self):
        create_project("test_project","test_project_desc",'Open')
        response = self.client.get(reverse('repositories_app:projects_app:main',kwargs={'repository_id':1}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual(response.context['projects'],['<Project: test_project>'])

    def test_valid_project_details(self):
        test_project = create_project("test_project","test_project_desc",'Open')
        response = self.client.get(reverse('repositories_app:projects_app:project',kwargs={'repository_id':1,'project_id': test_project.id}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual([response.context['project']],['<Project: test_project>'])

    def test_invalid_project_details(self):
        response = self.client.get(reverse('repositories_app:projects_app:project',kwargs={'repository_id':1,'project_id': 2}))
        self.assertEquals(response.status_code,302)

    def test_private_repo_project_details(self):
        test_project = create_project("test_project","test_project_desc",'Open')      
        test_project.repository.is_public = False  
        test_project.repository.save()    
        response = self.client.get(reverse('repositories_app:projects_app:project',kwargs={'repository_id':1,'project_id': test_project.id}))
        self.assertEquals(response.status_code,302)

    def test_close_project(self):  
        self.client.login(username='temporary', password='temporary')
        test_project = create_project("test_project","test_project_desc",'Open')         
        response = self.client.get(reverse('repositories_app:projects_app:close_project',kwargs={'project_id':test_project.id,'repository_id':1}))
        test_project = Project.objects.get(id=test_project.id)
        self.assertEquals(test_project.status,'Closed')
    
    def test_reopen_project(self):  
        self.client.login(username='temporary', password='temporary')
        test_project = create_project("test_project","test_project_desc",'Closed')         
        response = self.client.get(reverse('repositories_app:projects_app:reopen_project',kwargs={'project_id':test_project.id,'repository_id':1}))
        test_project = Project.objects.get(id=test_project.id)
        self.assertEquals(test_project.status,'Open')
    
    def test_delete_valid_project(self):
        self.client.login(username='temporary', password='temporary')
        test_project = create_project("test_project","test_project_desc",'Open')         
        response = self.client.get(reverse('repositories_app:projects_app:delete_project',kwargs={'project_id':test_project.id,'repository_id':1}))
        exists = Project.objects.filter(id=test_project.id).exists()
        self.assertEquals(exists,False)

    def test_delete_invalid_project(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('repositories_app:projects_app:delete_project',kwargs={'project_id':2,'repository_id':1}))
        self.assertEquals(response.status_code,302)

class ProjectsFormTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_new_project_valid_form(self):
        form = ProjectForm(data={'name':'name','description':'desc','repository':create_repository()})
        self.assertTrue(form.is_valid())

    def test_new_project_post_valid_form(self):
        create_repository()
        self.client.login(username='temporary', password='temporary')
        response  = self.client.post(reverse("repositories_app:projects_app:new_project",kwargs={'repository_id':1}),data={'name':'name','description':'desc','repository':1})
        exists = Project.objects.filter(name='name').exists()
        self.assertTrue(exists)
        self.assertEquals(response.status_code,302)

    def test_new_project_post_invalid_form(self):
        create_repository()
        self.client.login(username='temporary', password='temporary')
        response  = self.client.post(reverse("repositories_app:projects_app:new_project",kwargs={'repository_id':1}),data={'name':'','description':'desc'})
        self.assertEquals(response.status_code,200)
        self.assertFormError(response,'form','name','This field is required.')

    def test_edit_project_name_post_valid_form(self):
        test_project = create_project("test_project","test_project_desc",'Open')         
        self.client.login(username='temporary', password='temporary')
        response  = self.client.post(reverse("repositories_app:projects_app:edit_project",kwargs={'repository_id':1,'project_id':test_project.id}),data={'name':'changed_name','description':'desc','repository':test_project.repository.id})
        test_project = Project.objects.get(id=test_project.id)
        self.assertEquals(test_project.name,'changed_name')
        self.assertEquals(response.status_code,302)

    def test_edit_project_description_post_valid_form(self):
        test_project = create_project("test_project","test_project_desc",'Open')         
        self.client.login(username='temporary', password='temporary')
        response  = self.client.post(reverse("repositories_app:projects_app:edit_project",kwargs={'repository_id':1,'project_id':test_project.id}),data={'name':'test_project','description':'changed_description','repository':test_project.repository.id})
        test_project = Project.objects.get(id=test_project.id)
        self.assertEquals(test_project.description,'changed_description')
        self.assertEquals(response.status_code,302)

    def test_edit_project_post_invalid_form_name_empty(self):
        test_project = create_project("test_project","test_project_desc",'Open')         
        self.client.login(username='temporary', password='temporary')
        response  = self.client.post(reverse("repositories_app:projects_app:edit_project",kwargs={'repository_id':1,'project_id':test_project.id}),data={'name':'','description':'desc','repository':test_project.repository.id})
        self.assertFormError(response,'form','name','This field is required.')
        
    def test_new_project_invalid_form_name_nonunique(self):
        test_project = create_project("test_project","test_project_desc",'Closed') 
        self.client.login(username='temporary', password='temporary')
        response  = self.client.post(reverse("repositories_app:projects_app:new_project",kwargs={'repository_id':1}),data={'name':'test_project','description':'desc','repository':test_project.repository.id})
        self.assertFormError(response,'form','name','Project with this name already exists in this repository')
