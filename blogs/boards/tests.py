from django.test import TestCase
from django.urls import reverse, resolve
from .views import home
from .views import board_topics, new_topic
from .models import Board, Topic, Post
from django.contrib.auth.models import User

from .forms import NewTopicForm

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
        
    def test_board_topics_view_contains_navigation_links(self):
        # get url from views using reverse for following:
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        
        response = self.client.get(board_topics_url)
        
        # check if the html linked to board_topics, topics.html (which is the response from board_topics_url), 
        # contains href link for opening homepage_url
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        # check if the html linked to board_topics, topics.html (which is the response from board_topics_url), 
        # contains href link for opening new_topic_url
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
        
        

class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board')
        User.objects.create_user(username='john', email='john@doe.com', password='123')  # <- included this line here
        
    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_new_topic_view_now_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)
        
    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
        
    # new tests 04/11 (errors in below tests)
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
        
    # NewTopicForm aako xa ki chaina check gareko
    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)