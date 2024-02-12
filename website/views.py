from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'website/index.html')


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'Login successes!')
    else:
        messages.error(request, 'Login failed!')
    return redirect('index')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successes!')
    return redirect('index')
