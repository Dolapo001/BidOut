import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from users.models import User
from .models import Auction, Bid, Category, Watchlist, Comment
from .forms import AuctionForm
from django.contrib import messages

# Create your views here.


def home(request):
    featured_items = Auction.objects.all()
    count = 6
    if featured_items.count() < 6:
        count = featured_items.count()
    featured_items = random.sample(list(featured_items), count)
    context = {"featured_items": featured_items}
    return render(request, "Home.html", context)

def auctions(request):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'auctions/auctions.html', context)


def auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = auction.bids.all()
    highest_bid = bids.first()
    num_bids = bids.count() if bids.exists() else 0
    auction_winner = None

    if auction.is_closed:
        if request.user.is_authenticated:
            if auction.winner == request.user:
                auction_winner = request.user
                messages.success(request, "Congratulations! You have won this auction.")
            else:
                return render(request, 'auctions/auction_closed.html', {'auction': auction})
        else:
            return render(request, 'auctions/auction_closed.html', {'auction': auction})

    if request.method == 'POST':
        if 'bid_amount' in request.POST:
            try:
                bid_amount = Decimal(request.POST['bid_amount'])
            except Decimal.InvalidOperation:
                bid_amount = None

            if bid_amount is not None and (highest_bid is None or bid_amount > highest_bid.amount):
                auction.current_bid = bid_amount
                auction.save()
                bid = Bid(auction=auction, bidder=request.user, amount=bid_amount)
                bid.save()
                messages.success(request, "Your bid has been placed successfully!")
            else:
                messages.error(request, "Your bid amount must be greater than the current highest bid.")
        elif 'comment' in request.POST:
            comment_content = request.POST['comment']
            comment = Comment(auction=auction, user=request.user, text=comment_content)
            comment.save()
            messages.success(request, "Your comment has been posted successfully.")
        return redirect('auction', pk=pk)

    comments = Comment.objects.filter(auction=auction)
    context = {
        'auction': auction,
        'bids': bids,
        'highest_bid': highest_bid.amount if highest_bid else None,
        'num_bids': num_bids if num_bids > 0 else 'No bids yet',
        'current_bid': auction.current_bid,
        'auction_winner': auction_winner,
    }
    return render(request, 'auctions/single-auction.html', context)


@login_required(login_url="login")
def createAuction(request):
    form = AuctionForm()

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('auctions')

    context = {'form': form}
    return render(request, "auctions/auction_form.html", context)


@login_required(login_url="login")
def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


@login_required(login_url="login")
def category_auctions(request, slug):
    category = get_object_or_404(Category, slug=slug)
    active_auctions = category.auction_set.filter(is_active=True)
    return render(request, "auctions/category_auctions.html", {"category": category, "active_auctions": active_auctions})


@login_required(login_url="login")
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    context = {'watchlist_items': watchlist_items}
    return render(request, 'auctions/watchlist.html', context)


@login_required(login_url="login")
def add_to_watchlist(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, auction=auction)

    if created:
        messages.success(request, "Item added to watchlist.")
    else:
        messages.info(request, "Item is already in the watchlist.")

    return redirect('watchlist')


@login_required(login_url="login")
def remove_from_watchlist(request, pk):
    watchlist_items = Watchlist.objects.filter(user=request.user, auction_id=pk)
    if watchlist_items.exists():
        watchlist_items.delete()
        messages.success(request, "Item removed from watchlist.")
    else:
        messages.error(request, "Item not found in watchlist.")
    return redirect('watchlist')


@login_required
def close_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    if request.method == 'POST':
        if auction.seller == request.user and not auction.is_closed:
            highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
            if highest_bid:
                auction.is_closed = True
                auction.winner = highest_bid.bidder
                auction.save()
                return redirect('won_auction', pk=auction.id)
            else:
                messages.warning(request, "The auction has no bids.")
        else:
            messages.error(request, "You are not authorized to close this auction or the auction is already closed.")
            return redirect('auction_detail', pk=auction.id)

    return render(request, 'auctions/close_auction.html', {'auction': auction})

@login_required
def won_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    is_winner = auction.winner == request.user if auction.is_closed else False
    if auction.is_closed and is_winner:
        context = {
            'auction': auction,
        }
        return render(request, 'auctions/won_auction.html', context)

    return redirect('auction_detail', pk=pk)


def user_auctions(request, username):
    user = get_object_or_404(User, username=username)
    auctions = Auction.objects.filter(seller=user)

    context = {
        'user': user,
        'auctions': auctions
    }

    return render(request, 'auctions/user_auctions.html', context)
