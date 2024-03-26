from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# logic for homepage
def home(request):
    # Response of logic
    return HttpResponse('Hello, World!')