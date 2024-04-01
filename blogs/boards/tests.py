from django.test import TestCase
from django.urls import reverse, resolve
from .views import home

# Create your tests here.

# To test if home page is working properly
class HomeTest(TestCase):
    
    # check succesful response from home by checking status code
    def test_home_view_status_code(self):
        # name='home' from urls.py for named url
        url = reverse('home')
        # get and store response in 'response' var
        response = self.client.get(url)
        # Test if Status code 200, succesful response
        self.assertEquals(response.status_code, 200)
        
    # is '/' (empty sub url: 192.169.0.0/) calling the same home func as the home func in views
    def test_home_url_resolves_home_view(self):
        # "/" refers to the same as url path '/' or '' (empty) sub url from urls.py path
        view = resolve("/")
        self.assertEquals(view.func, home)
        