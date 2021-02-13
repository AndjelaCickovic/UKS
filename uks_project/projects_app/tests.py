from django.test import TestCase
from django.urls import reverse
from projects_app.models import Project
from repositories_app.models import Repository

def create_repository():
    rep = Repository()
    rep.id = 1
    rep.is_public = True
    rep.name='test_repository'
    rep.save()
    return rep

def create_project(name, description):
    return Project.objects.create(name=name,description=description, repository=create_repository())

# Create your tests here.
class ProjectsViewTests(TestCase):
    
    def test_no_projects(self):
        create_repository()
        response = self.client.get(reverse('repositories_app:projects_app:main',kwargs={'repository_id':1}))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,"")
        self.assertQuerysetEqual(response.context['projects'],[])

    def test_projects(self):
        create_project("test_project","test_project_desc")
        response = self.client.get(reverse('repositories_app:projects_app:main',kwargs={'repository_id':1}))
        self.assertQuerysetEqual(response.context['projects'],['<Project: test_project>'])

    
    
