from django.test import TestCase
from repositories_app.models import Repository
from users.models import AppUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

# Create your tests here.

def create_user(username,first_name,last_name,password,email):
    User = get_user_model()
    user = User.objects.create_user(username,email,password)
    user.first_name=first_name
    user.last_name=last_name
    user.save()
    return AppUser.objects.create(user=user)

class UsersFormTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('test', 'test@gmail.com', 'test')

    def test_register_user_valid_form(self):
        response  = self.client.post(reverse("users:register",kwargs={}),data={'first_name':'Test1','last_name':'Test','username':'test1','password':'test1','confirm_password':'test1','email':'test.test@gmail.com'})
        self.assertTrue(User.objects.filter(username='test1').exists())
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.context['registered'],True)

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
        user = create_user('test1','test','test','test','test@gmail.com')
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
    
    def test_edit_profile_with_password_valid_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'Test2','last_name':'Test2','old_password':'test2','password':'test3','confirm_password':'test3','email':'test2@gmail.com'})
        user = AppUser.objects.get(id=user.id)
        self.assertContains(response,'Data successfully updated.')
        self.assertEquals(user.user.check_password('test3'),True)
    
    def test_edit_profile_with_no_password_valid_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'NameChanged','last_name':'SurnameChanged','email':'test2@gmail.com'})
        user = AppUser.objects.get(id=user.id)
        self.assertContains(response,'Data successfully updated.')
        self.assertEquals(user.user.first_name,'NameChanged')
        self.assertEquals(user.user.last_name,'SurnameChanged')

    def test_edit_profile_invalid_first_name_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'','last_name':'Test2','old_password':'test2','password':'test2','confirm_password':'test2','email':'test2@gmail.com'})
        self.assertFormError(response,'form','first_name','This field is required.')
    
    def test_edit_profile_invalid_old_password_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'Test2','last_name':'Test2','old_password':'test','password':'test2','confirm_password':'test2','email':'test2@gmail.com'})
        self.assertFormError(response,'form','old_password','Old password is not correct.')

    def test_edit_profile_invalid_old_password_empty_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'Test2','last_name':'Test2','old_password':'','password':'test2','confirm_password':'test2','email':'test2@gmail.com'})
        self.assertFormError(response,'form','old_password','Please submit value for old password.')

    def test_edit_profile_invalid_confirm_password_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'Test2','last_name':'Test2','old_password':'test2','password':'test','confirm_password':'test2','email':'test2@gmail.com'})
        self.assertFormError(response,'form','confirm_password','Passwords do not match.')

    def test_edit_profile_invalid_new_password_form(self):

        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        self.client.login(username='test2',password='test2')
        response  = self.client.post(reverse("users:edit_profile",kwargs={}),data={'first_name':'Test2','last_name':'Test2','old_password':'test2','password':'','confirm_password':'test2','email':'test2@gmail.com'})
        self.assertFormError(response,'form','password','Invalid value for new password submitted.')

    def test_edit_profile_invalid_access(self):
        user = create_user('test2','Test2','Test2','test2','test2@gmail.com')
        response  = self.client.get(reverse("users:edit_profile",kwargs={}))
        self.assertEquals(response.status_code,302)

    def test_log_out_invalid_access(self):
        response  = self.client.get(reverse("users:user_logout",kwargs={}))
        self.assertEquals(response.status_code,302)
