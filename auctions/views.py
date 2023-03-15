from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Auction, Bid, Category
from .forms import AuctionForm, BidForm, CommentForm
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from decimal import Decimal, getcontext
# Create your views here.



def auctions(request, ):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'auctions/auctions.html', context)


def auction(request, pk):
    form = CommentForm
    auction = Auction.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'bid' in request.POST:
                bid_form = BidForm(request.POST)
                if bid_form.is_valid():
                    bid = bid_form.save(commit=False)
                    bid.bidder = request.user
                    bid.listing = auction
                    bid.save()
                    messages.success(request, 'Bid added successfully.')
                    return redirect('listing', pk=auction.pk)
            elif 'comment' in request.POST:
                Commentform = CommentForm(request.POST)
                if Commentform.is_valid():
                    comment = Commentform.save(commit=False)
                    comment.user = request.user
                    comment.listing = auction
                    comment.save()
                    messages.success(request, 'Comment added successfully.')
                    return redirect('listing', pk=auction.pk)
        else:
            messages.warning(request, 'You must be logged in to bid or comment.')
    else:
        context = {'form': form, 'auction': auction, 'CommentForm': CommentForm}
    return render(request, 'auctions/single-auction.html', context)


def createAuction(request):
    form = AuctionForm()

    if request.method == 'POST':
        form = AuctionForm(request.POST)
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
            form.save()
            bid_amount = form.cleaned_data['bid_amount']
            if bid_amount > auction.current_bid:
                getcontext().prec = 10  # Set decimal context with 10 digit precision
                bid_amount = Decimal(str(bid_amount))  # Convert to Decimal
                bid = Bid(auction=auction, bidder=request.user, amount=bid_amount)
                bid.save()
                auction.current_bid = bid_amount
                auction.save()
                return redirect('auctions')
            else:
                messages.error(request, 'Bid must be greater than current bid.')
    else:
        form = BidForm()
    context = {'form': form, 'auction': auction}
    return render(request, 'auctions/place_bid.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'auctions/categories.html', context)


def auctionCategory(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    auctions = Auction.objects.filter(category=category, active=True)
    query = request.GET.get('q')
    if query:
        auctions = auctions.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(seller__username__icontains=query)
        ).distinct()
    context = {'category': category, 'auctions': auctions}
    return render(request, 'auctions/auction_category.html', context)




