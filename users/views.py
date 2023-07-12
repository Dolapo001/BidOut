from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.csrf import csrf_protect


User = get_user_model()


def dashboard(request):
    return render(request, "users/dashboard.html")


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            print('Username does not exist')
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('Username or password is incorrect')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
