from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auction
from .forms import AuctionForm
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

