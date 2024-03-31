from django.shortcuts import render
from django.http import HttpResponse

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
