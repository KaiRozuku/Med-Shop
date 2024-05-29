from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Drug, Cart, Category, Profile


class MainAppTests(TestCase):
    def setUp(self):
        # Set up a user for authentication tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Set up some data for testing
        self.category = Category.objects.create(name="Test Category")
        self.drug = Drug.objects.create(name="Test Drug", price=10.0, category=self.category)


    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
