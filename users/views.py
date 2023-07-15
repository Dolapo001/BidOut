from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from users.models import User
from django.contrib.auth.models import User
from auctions.models import Auction, Watchlist
User = get_user_model()


@login_required
def profile(request):
    user = request.user

    # Retrieve the number of auctions in the user's watchlist
    watchlist_count = Watchlist.objects.filter(user=user).count()

    # Retrieve the number of closed auctions
    closed_auctions_count = Auction.objects.filter(seller=user, is_active=False).count()

    # Retrieve the list of auctions won by the user
    won_auctions = Auction.objects.filter(winner=user)

    context = {
        'user': user,
        'watchlist_count': watchlist_count,
        'closed_auctions_count': closed_auctions_count,
        'won_auctions': won_auctions,
    }

    return render(request, 'users/profile.html', context)


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


def signup_View(request, **extra_fields):
    if request.method == "POST":
        first_name = request.POST.get("first-name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            messages.error(request, "Passwords don't match")
            return render(request, 'users/signup.html')

        try:
            user_fields = {**extra_fields, "first_name": first_name}
            user = User.objects.create_user(username, email, password, **user_fields)
            user.save()
        except IntegrityError:
            messages.info(request, "Username has already been taken")
            return render(request, "users/signup.html")

        login(request, user)
        messages.success(request, "Logged in successfully")
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "users/signup.html")
