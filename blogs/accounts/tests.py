from django.test import TestCase

# Create your tests here.

from django.urls import resolve, reverse
from .views import signup

class SignUpTests(TestCase):
    # test success respose status code
    def test_signup_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test if the view func called by the url /signup/ is the same view func named signup
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)
        
    