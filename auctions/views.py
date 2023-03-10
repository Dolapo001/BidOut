from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


Listing = [
    {'id': '1',
     'title':"Brand New royal Enfield 250 CC For special Sale",
     'description': 'Korem ipsum dolor amet, consectetur adipiscing elit. Maece nas in pulvinar neque. Nulla finibus lobortis pulvinar. Donec a consectetur nulla',
     'bidding_price': '$456.00'},
    {'id': '2',
     'title':"Brand New royal Enfield 250 CC For special Sale",
     'description': 'Korem ipsum dolor amet, consectetur adipiscing elit. Maece nas in pulvinar neque. Nulla finibus lobortis pulvinar. Donec a consectetur nulla',
     'bidding_price': '$456.00'},
    {'id': '3',
     'title':"Brand New royal Enfield 250 CC For special Sale",
     'description': 'Korem ipsum dolor amet, consectetur adipiscing elit. Maece nas in pulvinar neque. Nulla finibus lobortis pulvinar. Donec a consectetur nulla',
     'bidding_price': '$456.00'},


]



def auctions(request):
    page = 'auctions'
    number = 10
    context = {'page': page, 'number': number, 'auctions': Listing}
    return render(request, 'auctions/auctions.html', context)


def auction(request, pk):
    auctionObj = None
    for i in Listing:
        if i['id'] == pk:
            auctionObj = i
    return render(request, 'auctions/single-auction.html', {'auction': auctionObj})
