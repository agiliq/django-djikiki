
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class DjikikiAppTestcase(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            username="admin", email="admin@agiliq.com", password="admin")

    def test_DjikikiIndexView(self):
    	response = self.c.get(reverse("djikiki_index"))
    	self.assertEqual(302, response.status_code)
    	self.c.login(username="admin", password="admin")
    	self.assertEqual(302, response.status_code)

    def test_CreateView(self):
    	response = self.c.get(reverse("djikiki_create"))
    	self.assertEqual(302, response.status_code)
    	self.c.login(username="admin", password="admin")
    	self.assertEqual(302, response.status_code)    

    def test_FeaturedView(self):
    	response = self.c.get(reverse("djikiki_featured"))
    	self.assertEqual(200, response.status_code)
    	self.c.login(username="admin", password="admin")
    	self.assertEqual(200, response.status_code)    

    def test_CreateFeaturedView(self):
    	response = self.c.get(reverse("djikiki_create_featured"))
    	self.assertEqual(302, response.status_code)
    	self.c.login(username="admin", password="admin")
    	self.assertEqual(302, response.status_code)    

