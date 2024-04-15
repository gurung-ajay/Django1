from django.contrib.auth import login as auth_login

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# instead of using predefined UserCreationForm, importing our own customized UserCreationForm from forms.py
from .forms import SignUpForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})