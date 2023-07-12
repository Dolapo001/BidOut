from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import AbstractUserSIForm


User = get_user_model()


@login_required(login_url="login")
def dashboard(request):
    return render(request, "users/dashboard.html")


@csrf_protect
def login_view(request):
               
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.error(request, 'User has been logged out.')
    return redirect('login')


def signup_view(request):
    page = 'register'
    form = UserSignupForm()
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account has been created!')

    context = {'page': page}
    return render(request, 'users/signup.html', context)
