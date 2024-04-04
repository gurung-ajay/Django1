from django.test import TestCase
from django.urls import reverse, resolve
from .views import home
from .views import board_topics
from .models import Board

# Create your tests here.

# To test if home page is working properly
class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django.board')
        url = reverse('home')
        self.response = self.client.get(url)
    
    
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
        
    # check to see if there is hyper link (href) in home page to link to topics page for each topics clicked
    def test_home_view_contains_link_top_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
        
        
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
        
    # test what the server says if we access object in board object that isn't present with id 99
    # intentionally giving error to check if it gives appropriate response status code 404
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        # does it give 404 eror? checking it
        self.assertEqual(response.status_code, 404)
        
    
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        # check whether view function board_topics acquired by using resolve(from url) is the same as the one in views.py
        self.assertEqual(view.func, board_topics)
        
    # check to see of there is an href link in topics page to link back to home page
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))