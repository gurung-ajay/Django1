from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from .models import Board
from .models import Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Board

from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# replacement for classbased view for home
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


# This view is for when user opens url link ip/boards/1/ it opens value of objects with primamry key 1, "Django",
# and when opened ip/boards/2/ it opens value of objects with primary key 2 "Python"
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20) # displays 20 data in a page at once

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})

def about(request):
    return render(request, 'about.html')


def question(request, pk):
    return HttpResponse(f"Question: {pk}")

def post(request, slug):
    return HttpResponse(f"Slug: {slug}")

def blog_post(request, slug, pk):
    return HttpResponse(f"Blog_post: {slug} and PK: {pk}")

def user_profile(request, username):
    return HttpResponse(f"User Name: {username}")

def year_archive(request, year):
    return HttpResponse(f"Year: {year}")

# def new_topic(request, pk):
#     # similar logic as board_topics view funcion
#     # get board objects for given pk and if not found give 404 error
#     board = get_object_or_404(Board, pk=pk)
    
#     # when user inserts data and click post button, the post method will send data through http request
#     # these data will be captured and stored here
#     if request.method=="POST":
#         subject = request.POST['subject']
#         message = request.POST['message']
        
#         user = User.objects.first() # TODO: get the currently logged in user
        
#         # add data to the topic model
#         topic = Topic.objects.create(
#             subject = subject,
#             board = board,
#             starter = user
#         )

#         # add data to the post model
#         post = Post.objects.create(
#             message = message,
#             topic = topic,
#             created_by = user
#         )
        
#         return redirect('board_topics', pk=board.pk) # TODO: redirect to the created topic page
    
#     return render(request, 'new_topic.html', {'board': board})

# REPLACE new_topic as:
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    
    # For demonstration purposes, fetch the first user from the database.
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            # get current user
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                # get current user
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20    # number of data in a page displayed at once

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset
    
    
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})



# CLASS BASED VIEWS
class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'new_post.html'
   
    
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)