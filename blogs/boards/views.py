from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Board

# Create your views here.

# logic for homepage
def home(request):
    # Response of logic
    
    # access board objects(data) from database
    boards = Board.objects.all()
    #boards_names = []
    # store board names using loop in list
    #for board in boards:
    #    boards_names.append(board.name)
        
    # joins boards_names from list as one string    
    #response_html = '<br>'.join(boards_names)
    
    
    # render home.html and send boards variable data
    return render(request, 'home.html', {'boards' : boards})

# This view is for when user opens url link ip/boards/1/ it opens value of objects with primamry key 1, "Django",
# and when opened ip/boards/2/ it opens value of objects with primary key 2 "Python"
def board_topics(request, pk):
    # Accessing primary key from board objects to uniquely identify each objects
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})

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