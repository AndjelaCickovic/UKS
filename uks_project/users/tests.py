from django.test import TestCase
from repositories_app.models import Repository
from users.models import AppUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

# Create your tests here.


def create_user(username,first_name,last_name,password,email):
    User = get_user_model()
    user = User.objects.create_user(username,email,password)
    user.first_name=first_name
    user.last_name=last_name
    user.save()
    return AppUser.objects.create(user=user)



class UsersViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test')



class UsersFormTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test')

    def test_register_user_valid_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'Test','username':'test1','password':'test1','confirm_password':'test1','email':'test.test@gmail.com'})
        self.assertEquals(response.status_code,200)
        self.assertTrue(response,'registered')

    def test_register_user_invalid_first_name_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'','last_name':'Test','username':'test1','password':'test1','confirm_password':'test1','email':'test.test@gmail.com'})
        self.assertFormError(response,'user_form','username',[])
        self.assertFormError(response,'user_form','first_name','This field is required.')

    
    def test_register_user_invalid_last_name_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'','username':'test1','password':'test1','confirm_password':'test1','email':'test.test@gmail.com'})
        self.assertFormError(response,'user_form','last_name','This field is required.')

    def test_register_user_invalid_confirm_password_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'Test','username':'test1','password':'test','confirm_password':'test1','email':'test.test@gmail.com'})
        self.assertFormError(response,'user_form','confirm_password','Passwords do not match.')

    def test_register_user_invalid_email_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'Test','username':'test1','password':'test','confirm_password':'test1','email':'somemail.com'})
        self.assertFormError(response,'form','email','Enter a valid email address.')
    
    def test_register_user_invalid_username_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'Test','username':'test1','password':'test1','confirm_password':'test1','email':'test.test@gmail.com'})
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'Test','username':'test1','password':'test1','confirm_password':'test1','email':'test.test@gmail.com'})

        self.assertFormError(response,'user_form','username','A user with that username already exists.')

    def test_login_user_valid_form(self):
        response  = self.client.post(reverse("users:user_login",kwargs={}),data={'username':'test','password':'test'})
        self.assertEquals(response.status_code,302)

    def test_login_user_invalid_username_form(self):
        response  = self.client.post(reverse("users:user_login",kwargs={}),data={'username':'testt','password':'test'})
        self.assertContains(response,'Invalid login details supplied!')

    def test_login_user_invalid_password_form(self):
        response  = self.client.post(reverse("users:user_login",kwargs={}),data={'username':'test','password':'tesst'})
        self.assertContains(response,'Invalid login details supplied!')
