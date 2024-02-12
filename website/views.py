from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
# Create your views here.


def index(request):
    return render(request, 'website/index.html')


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successes!')
            else:
                messages.error(request, 'Invalid username or password!')
        else:
            messages.error(request, 'Invalid username or password!')
        return redirect('index')
    form = AuthenticationForm()
    return render(request, 'website/login.html', {'login_form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successes!')
    return redirect('index')

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(request, username=username, password=password)
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successes!')
            return redirect('index')
        messages.error(request, 'Registration failed!')
    form = NewUserForm()
    return render(request=request, template_name='website/register.html', context={"register_form": form})