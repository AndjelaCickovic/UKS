from django.test import TestCase
from django.urls import reverse
from issues_app.models import Label
from repositories_app.models import Repository
from issues_app.forms import LabelForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

def create_repository():
    repository = Repository(id = 1, is_public = True, name = 'test_repository')
    repository.save()
    return repository

def create_label(name, description, colour):
    return Label.objects.create(name = name, description = description, colour = colour, 
    repository = create_repository())

# Create your tests here.
class LabelsViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temp', 'temp@gmail.com', 'temp')

    def test_no_labels(self):
        create_repository()
        response = self.client.get(reverse('repositories_app:issues_app:labels', kwargs={'repository_id': 1}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual(response.context['test_labels'],[])

    def test_labels(self):
        create_label("test_label", "test_label_desc", "#AAAAAA")
        response = self.client.get(reverse('repositories_app:issues_app:labels', kwargs={'repository_id': 1}))
        self.assertEquals(response.status_code,200)
        self.assertQuerysetEqual(response.context['test_labels'],['<Label: test_label>'])
    
    def test_delete_valid_label(self):
        self.client.login(username='temp', password='temp')
        test_label = create_label("test_label", "test_label_desc", "#AAAAAA")         
        response = self.client.get(reverse('repositories_app:issues_app:delete_label', kwargs={'repository_id': 1, 'label_id': test_label.id}))
        exists = Label.objects.filter(id = test_label.id).exists()
        self.assertEquals(exists, False)

    def test_delete_invalid_label(self):
        self.client.login(username='temp', password='temp')
        response = self.client.get(reverse('repositories_app:issues_app:delete_label',kwargs={'repository_id': 1, 'label_id': 2}))
        self.assertEquals(response.status_code, 302)

class LabelsFormTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temp', 'temp@gmail.com', 'temp')

    def test_add_label_valid_form(self):
        form = LabelForm(data = {'name': 'test_label', 'description': 'test_label_desc', 'colour': '#AAAAAA', 'repository': create_repository()})
        self.assertTrue(form.is_valid())

    def test_add_label_post_valid_form(self):
        create_repository()
        self.client.login(username='temp', password='temp')
        response  = self.client.post(reverse("repositories_app:issues_app:add_label", kwargs={'repository_id': 1}), data={'name':'test_label', 'description':'test_label_desc', 'colour': '#AAAAAA'})
        self.assertEquals(response.status_code,200)
        self.assertFormError(response, 'form', 'name', None)
        self.assertFormError(response, 'form', 'description', None)
        self.assertFormError(response, 'form', 'colour', None)

    def test_add_label_post_invalid_form(self):
        create_repository()
        self.client.login(username='temp', password='temp')
        response  = self.client.post(reverse("repositories_app:issues_app:add_label", kwargs={'repository_id': 1}), data={'name':'', 'description':'test_label_desc', 'colour': '#AAAAAA'})
        self.assertEquals(response.status_code,200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_edit_label_post_valid_form(self):
        test_label = create_label("test_label", "test_label_desc", "#AAAAAA")         
        self.client.login(username='temp', password='temp')
        response  = self.client.post(reverse("repositories_app:issues_app:edit_label", kwargs={'repository_id': 1, 'label_id': test_label.id}), data={'name':'test_label_2', 'description':'test_label_desc_2', 'colour': '#BBBBBB'})
        self.assertFormError(response, 'form', 'name', None)
        self.assertFormError(response, 'form', 'description', None)
        self.assertFormError(response, 'form', 'colour', None)

    def test_edit_label_post_invalid_form(self):
        test_label = create_label("test_label", "test_label_desc", "#AAAAAA")       
        self.client.login(username='temp', password='temp')
        response  = self.client.post(reverse("repositories_app:issues_app:edit_label", kwargs={'repository_id': 1, 'label_id': test_label.id}), data={'name':'', 'description':'test_label_desc', 'colour': '#AAAAAA'})
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        
