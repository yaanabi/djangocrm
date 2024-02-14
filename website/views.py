from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import NewUserForm, NewRecordForm
from .models import Record
# Create your views here.


def index(request):
    return render(request, 'website/index.html',)


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
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successes!')
            return redirect('index')
        messages.error(request, 'Registration failed!')
    form = NewUserForm()
    return render(request=request, template_name='website/register.html', context={"register_form": form})


def make_record(request):
    if request.method == 'POST':
        form = NewRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your data have been saved!')
            return redirect('index')
        messages.error(request, 'Your data is incorrect!')
        return redirect('record')
    form = NewRecordForm()
    return render(request, 'website/create_record.html', {'record_form': form})


def show_records(request):
    if request.method == "GET":
        query = request.GET.get('q')
        if query:
            records_list = Record.objects.filter(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(city__icontains=query)|Q(phone__icontains=query)\
                                                |Q(created_at__icontains=query))
            return render(request, 'website/show_records.html', {'records':records_list})
    records = Record.objects.all()
    return render(request, 'website/show_records.html', {'records': records})