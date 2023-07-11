from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .models import User

User = get_user_model()


def dashboard(request):
    return render(request, "users/dashboard.html")


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email_or_username = request.POST['email_or_username']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            print('Username or Email does not exist')
        user = authenticate(request, email=email_or_username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            print('Username/email or password is incorrect')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
