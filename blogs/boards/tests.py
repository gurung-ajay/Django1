from django.test import TestCase
from django.urls import reverse, resolve
from .views import home
from .models import Board

# Create your tests here.

# To test if home page is working properly
class HomeTest(TestCase):
    # normally django locates views function from location set in url,
	# but during reverse, it does the opposite, given a views function, it will find its url.
    # check succesful response from home by checking status code
    def test_home_view_status_code(self):
        # name='home' from urls.py for named url
        url = reverse('home')
        # get and store response in 'response' var
        response = self.client.get(url)
        # Test if Status code 200, succesful response
        self.assertEqual(response.status_code, 200)
        
    # is '/' (empty sub url: 192.169.0.0/) calling the same home func as the home func in views
    def test_home_url_resolves_home_view(self):
        # "/" refers to the same as url path '/' or '' (empty) sub url from urls.py path
        # resolve returns the views function linked with url path given in the parameter in urls.py
        view = resolve("/")
        # check whether view function acquired by using resolve(from url) is the same as the one in views.py
        self.assertEqual(view.func, home)
        
        
class BoardTopicsTests(TestCase):
    # create a dumy object in boards
    def setUp(self):
        Board.objects.create(name='Django', description='Django Board.')
        
    # check to see if the httpresponse was a success when running '/board_topics/1/'
    def test_board_topics_view_success_status_code(self):
        # this means '/board_topics/1/'
        url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)