from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Auction, Bid
from .forms import AuctionForm, BidForm
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from decimal import Decimal, getcontext
# Create your views here.



def auctions(request, ):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'auctions/auctions.html', context)


def auction(request, pk):
    auction_obj = Auction.objects.get(id=pk)
    num_bids = auction_obj.bids.count()
    context = {'auction': auction_obj, 'num_bids': num_bids}
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
    return render(request, 'auctions/place_bid.html', {'form': form, 'auction': auction})









