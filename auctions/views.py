import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Auction, Bid, Category, Watchlist
from .forms import AuctionForm, BidForm, CommentForm
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from decimal import Decimal, getcontext

# Create your views here.


def home(request):
    featured_items = Auction.objects.all()
    count = 6
    if featured_items.count() < 6:
        count = featured_items.count()
    featured_items = random.sample(list(featured_items), count)
    context = {"featured_items": featured_items}
    return render(request, "Home.html", context)


def auctions(request, ):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'auctions/auctions.html', context)


def auction(request, pk):
        auction = get_object_or_404(Auction, id=pk)
        context = {
            'auction': auction
        }
        return render(request, 'auctions/single-auction.html', context)


def createAuction(request):
    form = AuctionForm()

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('auctions')

    context = {'form': form}
    return render(request, "auctions/auction_form.html", context)


@transaction.atomic
def placeBid(request, pk):
    auction = Auction.objects.get(id=pk)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            if bid_amount > auction.current_bid:
                getcontext().prec = 10
                bid_amount = Decimal(str(bid_amount))
                bid = Bid(auction=auction, bidder=request.user, amount=bid_amount)
                bid.save()
                auction.current_bid = bid_amount
                auction.save()
                form.save()
                return redirect('auction')
            else:
                messages.error(request, 'Bid must be greater than current bid.')
    else:
        form = BidForm()
    context = {'form': form, 'auction': auction}
    return render(request, 'auctions/place_bid.html', context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category_auctions(request, slug):
    category = get_object_or_404(Category, slug=slug)
    active_auctions = category.auction_set.filter(is_active=True)
    return render(request, "auctions/category_auctions.html", {"category": category, "active_auctions": active_auctions})

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    context = {'watchlist_items': watchlist_items}
    return render(request, 'auctions/watchlist.html', context)

@login_required
def add_to_watchlist(request, pk):
    watchlist_item = Watchlist(user=request.user, pk=id)
    watchlist_item.save()
    return redirect('watchlist')


@login_required
def remove_from_watchlist(request, pk):
    watchlist_item = Watchlist.objects.get(user=request.user, pk=id)
    watchlist_item.delete()
    return redirect('watchlist')


