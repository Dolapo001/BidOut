from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.csrf import csrf_protect


User = get_user_model()


def dashboard(request):
    return render(request, "users/dashboard.html")


@csrf_protect
def login_view(request):
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
            return redirect('home')
        else:
            print('Username/email or password is incorrect')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
