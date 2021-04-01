import os
import re
import inspect
import tempfile
import website.models
from website import forms
from website import views
from populate_skyview import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from website.models import UserProfile, Post, Planet
from django.forms import fields as django_fields
from django.template.defaultfilters import slugify
from django.forms import ModelChoiceField


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_user_profile_object():
    """
    Helper function to create a UserProfile object.
    """
    user = UserProfile.objects.get_or_create(user=create_user_object(),
                                      website="",
                                      picture="")[0]
    user.save()

    return user

def get_template(path_to_template):
    """
    Helper function to return the string representation of a template file.
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str

class ModelTest(TestCase):

    def test_userprofile_class(self):
            """
            Does the UserProfile class exist in website.models? If so, are all the required attributes present?
            """
            self.assertTrue('UserProfile' in dir(website.models))

            user_profile = website.models.UserProfile()

            expected_attributes = {
                'website': 'www.google.com',
                'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
                'user': create_user_object(),
            }

            expected_types = {
                'website': models.fields.URLField,
                'picture': models.fields.files.ImageField,
                'user': models.fields.related.OneToOneField,
            }

            found_count = 0

            for attr in user_profile._meta.fields:
                attr_name = attr.name

                for expected_attr_name in expected_attributes.keys():
                    if expected_attr_name == attr_name:
                        found_count += 1

                        self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. {FAILURE_FOOTER}")
                        setattr(user_profile, attr_name, expected_attributes[attr_name])
            
            self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. {FAILURE_FOOTER}")
            user_profile.save()

class RegisterFormClassTests(TestCase):

    def test_user_form(self):
            """
            Tests whether UserForm is in the correct place, and whether the correct fields have been specified for it.
            """
            self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserForm class in forms.py module. {FAILURE_FOOTER}")
            
            user_form = forms.UserForm()
            self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}UserForm does not match up to the User model.{FAILURE_FOOTER}")

            fields = user_form.fields
            
            expected_fields = {
                'username': django_fields.CharField,
                'email': django_fields.EmailField,
                'password': django_fields.CharField,
            }
            
            for expected_field_name in expected_fields:
                expected_field = expected_fields[expected_field_name]

                self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserForm form. {FAILURE_FOOTER}")
                self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")
        
    def test_user_profile_form(self):
            """
            Tests whether UserProfileForm is in the correct place, and whether the correct fields have been specified for it.
            """
            self.assertTrue('UserProfileForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserProfileForm class in forms.py module. {FAILURE_FOOTER}")
            
            user_profile_form = forms.UserProfileForm()
            self.assertEqual(type(user_profile_form.__dict__['instance']), website.models.UserProfile, f"{FAILURE_HEADER} UserProfileForm does not match up to the UserProfile model.{FAILURE_FOOTER}")

            fields = user_profile_form.fields

            expected_fields = {
                'website': django_fields.URLField,
                'picture': django_fields.ImageField,
            }

            for expected_field_name in expected_fields:
                expected_field = expected_fields[expected_field_name]

                self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserProfile form.{FAILURE_FOOTER}")
                self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

class RegistrationTests(TestCase):

    def test_new_registration_view_exists(self):
        """
        Checks to see if the new registration view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('website:signUp')
        except:
            pass
        
        self.assertEqual(url, '/signUp/', f"{FAILURE_HEADER}Incorrent URL mapping for Sign Up.{FAILURE_FOOTER}")
    
    def test_registration_template(self):
        """
        Does the signUp.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'signUp.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'signUp.html' template.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)Sign Up(\s*|\n*)-(\s*|\n*)SkyView(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Sign Up(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('website:signUp'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'website:signUp' is not correct. {FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Incorrect title_block.{FAILURE_FOOTER}")

    def test_registration_get_response(self):
        """
        Checks the GET response of the registration view.
        """
        request = self.client.get(reverse('website:signUp'))
        content = request.content.decode('utf-8')

        self.assertTrue('action="/signUp/"' in content, f"{FAILURE_HEADER}Incorrect URL pointing for <form> in signUp.html{FAILURE_FOOTER}")
        self.assertTrue('<button class="button button-large">Sign Up</button>' in content, f"{FAILURE_HEADER}Incorrect markup for the form submission button in signUp.html.{FAILURE_FOOTER}")
   
    def test_bad_registration_post_response(self):
        """
        Checks the POST response of the registration view.
        """
        request = self.client.post(reverse('website:signUp'))
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)
    
    def test_good_form_creation(self):
        """
        Tests the functionality of the forms.
        Creates a UserProfileForm and UserForm, and attempts to save them.
        """
        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm was not valid after entering the required data. {FAILURE_FOOTER}")
        self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data. {FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()
        
        user_profile_object = user_profile_form.save(commit=False)
        user_profile_object.user = user_object
        user_profile_object.save()
        
        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}User object was not created.{FAILURE_FOOTER}")
        self.assertEqual(len(website.models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER}UserProfile object was not created.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}Sample user could not be logged in.{FAILURE_FOOTER}")
    
    def test_good_registration_post_response(self):
        """
        Checks the POST response of the registration view.
        """
        post_data = {'username': 'webformuser', 'password': 'test123', 'email': 'test@test.com', 'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        request = self.client.post(reverse('website:signUp'), post_data)
        content = request.content.decode('utf-8')

        self.assertTrue(self.client.login(username='webformuser', password='test123'), f"{FAILURE_HEADER}User could not be logged in after using the registration form.{FAILURE_FOOTER}")

    def test_base_for_register_link(self):
        """
        Tests whether the registration link has been added to the base.html template.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        base_path = os.path.join(template_base_path, 'base.html')
        template_str = get_template(base_path)
        self.assertTrue('<a href="{% url \'website:signUp\' %}">Sign Up</a>' in template_str)

class LoginTests(TestCase):

    def test_login_url_exists(self):
        """
        Checks to see if the new login view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('website:login')
        except:
            pass
        
        self.assertEqual(url, '/login/', f"{FAILURE_HEADER}Incorrent URL mapping for Login.{FAILURE_FOOTER}")

    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in, and should be redirected to the homepage.
        """
        user_object = create_user_object()

        response = self.client.post(reverse('website:login'), {'username': 'testuser', 'password': 'testabc123'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}The attempt to log in through views was not successful.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging in was successful. However, got a status code of {response.status_code} instead of redirect.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('website:home'), f"{FAILURE_HEADER}We were not redirected to the homepage after logging in.{FAILURE_FOOTER}")

    def test_login_template(self):
        """
        Does the login.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)Login(\s*|\n*)-(\s*|\n*)SkyView(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('website:login'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'website:login' is not correct.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}The title_block is not correct.{FAILURE_FOOTER}")
    
    def test_login_template_content(self):
        """
        Some simple checks for the login.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('action="{% url \'website:login\' %}"' in template_str, f"{FAILURE_HEADER}Url lookup for 'website:login' not found in login.html <form>.{FAILURE_FOOTER}")
        self.assertTrue('<button class="button button-large">Login</button>' in template_str, f"{FAILURE_HEADER}Login button not found in login.html template.{FAILURE_FOOTER}")

class LogoutTests(TestCase):

    def test_bad_request(self):
        """
        Attepts to log out a user who is not logged in.
        This should according to the book redirect you to the login page.
        """
        response = self.client.get(reverse('website:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('website:login'))
    
    def test_good_request(self):
        """
        Attempts to log out a user who IS logged in.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. {FAILURE_FOOTER}")
        
        response = self.client.get(reverse('website:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('website:home'), f"{FAILURE_HEADER}Logging out a user should redirect them to the homepage.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out!{FAILURE_FOOTER}")

class LinkTidyingTests(TestCase):
    """
    Some checks to see whether the links in base.html have been tidied up and change depending on whether a user is logged in or not.
    """
    def test_omnipresent_links(self):
        """
        Checks for links that should always be present, regardless of user state.
        """
        content = self.client.get(reverse('website:home')).content.decode()
        self.assertTrue('href="/feed/"' in content)
        self.assertTrue('href="/planets/"' in content)

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        # These should be present.
        content = self.client.get(reverse('website:home')).content.decode()
        self.assertTrue('href="/feed/"' in content, f"{FAILURE_HEADER}The links in base.html are not correct.{FAILURE_FOOTER}")
        self.assertTrue('href="/planets/"' in content, f"{FAILURE_HEADER}The links in base.html are not correct.{FAILURE_FOOTER}")
    
    def test_logged_in_links(self):
        """
        Checks for links that should only be displayed when the user is logged in.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('website:home')).content.decode()

        # These should be present.
        self.assertTrue('href="/feed/create-post/"' in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged in.{FAILURE_FOOTER}")
        self.assertTrue('href="/login/my-profile"' in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged in.{FAILURE_FOOTER}")
        self.assertTrue('href="/logout/"' in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged in.{FAILURE_FOOTER}")

        # These should not be present.
        self.assertTrue('href="/login/"' not in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged in.{FAILURE_FOOTER}")
        self.assertTrue('href="/signUp/"' not in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged in.{FAILURE_FOOTER}")
    
    def test_logged_out_links(self):
        """
        Checks for links that should only be displayed when the user is not logged in.
        """
        content = self.client.get(reverse('website:home')).content.decode()

        # These should be present.
        self.assertTrue('href="/login/"' in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged out.{FAILURE_FOOTER}")
        self.assertTrue('href="/signUp/"' in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged out.{FAILURE_FOOTER}")
        
        # These should not be present.
        self.assertTrue('href="/feed/create-post/"' not in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged out.{FAILURE_FOOTER}")
        self.assertTrue('href="/login/my-profile"' not in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged out.{FAILURE_FOOTER}")
        self.assertTrue('href="/logout/"' not in content, f"{FAILURE_HEADER}The links in base.html are not correct when logged out.{FAILURE_FOOTER}")



class PostTests(TestCase):
    
    def test_create_post(self):
        """
        Tests to see if a post can be added when logged in.
        """
        populate()
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('website:create_post'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}No HTTP status code when attempting to add a page when logged in.{FAILURE_FOOTER}")
        
        content = response.content.decode()
        self.assertTrue('Create Post' in content, f"{FAILURE_HEADER}Adding a post doesn't result in the expected page.{FAILURE_FOOTER}")
    

    def test_create_post_link(self):
        """
        Tests to see if the Create Post link only appears when logged in.
        """
        content = self.client.get(reverse('website:home')).content.decode()

        self.assertTrue(reverse('website:create_post') not in content, f"{FAILURE_HEADER}The Create Post link was present when a user is not logged in.{FAILURE_FOOTER}")

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('website:home')).content.decode()

        self.assertTrue(reverse('website:create_post') in content, f"{FAILURE_HEADER}The Create Post link was not present.{FAILURE_FOOTER}")
    
    def test_create_post_url_exists(self):
        """
        Checks to see if the create_post view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('website:create_post')
        except:
            pass
        
        self.assertEqual(url, '/feed/create-post/', f"{FAILURE_HEADER}Incorrent URL mapping for Create Post.{FAILURE_FOOTER}")

    def test_create_post_title(self):
        """
        Does the createPost.html template exist in the correct place, and does it have the correct title block?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'createPost.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'createPost.html' template.{FAILURE_FOOTER}")

        template_str = get_template(template_path)

        block_title_pattern = r'{% block title_block %}(\s*|\n*)Create Post(\s*|\n*){% (endblock|endblock title_block) %}'

        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}The title_block is not correct.{FAILURE_FOOTER}")
        
        
    def test_create_post_template_content(self):
        """
        Some simple checks for the createPost.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'createPost.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'createPost.html' template.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('action="{% url \'website:create_post\' %}"' in template_str, f"{FAILURE_HEADER}Url lookup for 'website:createPost' not found in login.html <form>.{FAILURE_FOOTER}")
        self.assertTrue('<button class="button button-large">Create Post</button>' in template_str, f"{FAILURE_HEADER}Submit button not found in createPost.html template.{FAILURE_FOOTER}")


    def test_post_form(self):
            """
            Tests whether Post is in the correct place, and whether the correct fields have been specified for it.
            """
            self.assertTrue('Post' in dir(forms), f"{FAILURE_HEADER}We couldn't find the Post class in forms.py module. {FAILURE_FOOTER}")
            
            post_form = forms.PostForm()
            self.assertEqual(type(post_form.__dict__['instance']), Post, f"{FAILURE_HEADER}PostForm does not match up to the Post model.{FAILURE_FOOTER}")

            fields = post_form.fields
            
            expected_fields = {
                'planet': ModelChoiceField,
                'heading': django_fields.CharField,
                'image': django_fields.ImageField,
                'body':django_fields.CharField,
            }
            
            for expected_field_name in expected_fields:
                expected_field = expected_fields[expected_field_name]

                self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the PostForm form. {FAILURE_FOOTER}")
                self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in PostForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

class PlanetsTests(TestCase):

    def test_planets_url_exists(self):
        """
        Checks to see if the planets exist in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('website:planets')
        except:
            pass
        
        self.assertEqual(url, '/planets/', f"{FAILURE_HEADER}Incorrent URL mapping for Planets.{FAILURE_FOOTER}")

    def test_planets_template(self):
        """
        Does the planets.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'planets.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'planets.html' template.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)The Planets(\s*|\n*)-(\s*|\n*)SkyView(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)The Planets(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('website:planets'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'website:planets' is not correct.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}The title_block is not correct.{FAILURE_FOOTER}")

    def test_planets_template_content(self):
        """
        Some simple checks for the planets.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'planets.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'planets.html' template.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('{% url \'website:planet\' planet.slug %}' in template_str, f"{FAILURE_HEADER}Url lookup for 'website:planets' not found in planets.html <form>.{FAILURE_FOOTER}")
        self.assertTrue('{% for planet in planets %}' in template_str, f"{FAILURE_HEADER}Planets not found in login.html template.{FAILURE_FOOTER}")
        self.assertTrue('"{% url \'website:planet\' planet.slug %}"' in template_str, f"{FAILURE_HEADER}Planet links not found in login.html template.{FAILURE_FOOTER}")
        self.assertTrue('"{{ planet.image.url }}"' in template_str, f"{FAILURE_HEADER}Planet images not found in login.html template.{FAILURE_FOOTER}")


class PlanetTests(TestCase):

    def test_planet_earth_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Earth')})
        except:
            pass
        
        self.assertEqual(url, '/planets/earth/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Earth.{FAILURE_FOOTER}")
    
    def test_general_url_exists(self):
        """
        Checks to see if the general planet page exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('General')})
        except:
            pass
        
        self.assertEqual(url, '/planets/general/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet.{FAILURE_FOOTER}")

    def test_planet_mercury_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Mercury')})
        except:
            pass
        
        self.assertEqual(url, '/planets/mercury/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Mercury.{FAILURE_FOOTER}")

    
    def test_planet_venus_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Venus')})
        except:
            pass
        
        self.assertEqual(url, '/planets/venus/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Venus.{FAILURE_FOOTER}")

    
    def test_planet_mars_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Mars')})
        except:
            pass
        
        self.assertEqual(url, '/planets/mars/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Mars.{FAILURE_FOOTER}")

    
    def test_planet_jupiter_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Jupiter')})
        except:
            pass
        
        self.assertEqual(url, '/planets/jupiter/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Jupiter.{FAILURE_FOOTER}")

    def test_planet_saturn_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Saturn')})
        except:
            pass
        
        self.assertEqual(url, '/planets/saturn/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Saturn.{FAILURE_FOOTER}")

    def test_planet_uranus_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Uranus')})
        except:
            pass
        
        self.assertEqual(url, '/planets/uranus/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Uranus.{FAILURE_FOOTER}")

    def test_planet_neptune_url_exists(self):
        """
        Checks to see if the planet exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('website:planet', kwargs={'planet_name':slugify('Neptune')})
        except:
            pass
    
        self.assertEqual(url, '/planets/neptune/', f"{FAILURE_HEADER}Incorrent URL mapping for Planet Neptune.{FAILURE_FOOTER}")

    def test_planets_template_content(self):
        """
        Some simple checks for the planet.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'planet.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'planet.html' template.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('{{ planet.image.url }}' in template_str, f"{FAILURE_HEADER}{{ planet.image.url }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ planet.name }} Statistics' in template_str, f"{FAILURE_HEADER}{{ planet.name }} Statistics not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.mass }}' in template_str, f"{FAILURE_HEADER}{{ statistics.mass }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.diameter }}' in template_str, f"{FAILURE_HEADER}{{ statistics.diameter }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.volume }}' in template_str, f"{FAILURE_HEADER}{{ statistics.volume }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.gravity }}' in template_str, f"{FAILURE_HEADER}{{ statistics.gravity }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.averageTemperature }}' in template_str, f"{FAILURE_HEADER}{{ statistics.averageTemperature }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.numberOfMoons }}' in template_str, f"{FAILURE_HEADER}{{ statistics.numberOfMoons }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.averageDistanceFromSun }}' in template_str, f"{FAILURE_HEADER}{{ statistics.averageDistanceFromSun }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.lengthOfDay }}' in template_str, f"{FAILURE_HEADER}{{ statistics.lengthOfDay }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.lengthOfYear }}' in template_str, f"{FAILURE_HEADER}{{ statistics.lengthOfYear }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.contentsOfAtmosphere }}' in template_str, f"{FAILURE_HEADER}{{ statistics.contentsOfAtmosphere }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.water}}' in template_str, f"{FAILURE_HEADER}{{ statistics.water}} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('{{ statistics.specialties }}' in template_str, f"{FAILURE_HEADER}{{ statistics.specialties }} not found in planet.html template.{FAILURE_FOOTER}")
        self.assertTrue('Posts about {{ planet.name }}' in template_str, f"{FAILURE_HEADER}Posts not found in planet.html template.{FAILURE_FOOTER}")


class HomepageTests(TestCase):
    def test_home_url_exists(self):
        """
        Checks to see if the homepage exist in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('website:home')
        except:
            pass
        
        self.assertEqual(url, '/', f"{FAILURE_HEADER}Incorrent URL mapping for Homepage.{FAILURE_FOOTER}")

    def test_home_template(self):
        """
        Does the home.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'home.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'home.html' template.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)Start Your Journey(\s*|\n*)-(\s*|\n*)SkyView(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Start Your Journey(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('website:home'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'website:home' is not correct.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}The title_block is not correct.{FAILURE_FOOTER}")

    def test_home_template_content(self):
        """
        Some simple checks for the home.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'SkyView')
        template_path = os.path.join(template_base_path, 'home.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'home.html' template.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('{% planets_carousel %}' in template_str, f"{FAILURE_HEADER}Carousel not found in home.html.{FAILURE_FOOTER}")
        self.assertTrue('Feed' in template_str, f"{FAILURE_HEADER}Feed heading not found in login.html template.{FAILURE_FOOTER}")
        self.assertTrue('NASA Picture of the Day' in template_str, f"{FAILURE_HEADER}NASA heading not found in login.html template.{FAILURE_FOOTER}")
        self.assertTrue('"{% static \'scripts/nasaPictureOfTheDay.js\' %}"' in template_str, f"{FAILURE_HEADER}NASA picture not found in login.html template.{FAILURE_FOOTER}")