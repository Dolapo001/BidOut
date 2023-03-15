from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms
from .models import Auction, Bid, Comment


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'price', 'starting_bid']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction', None)
        super().__init__(*args, **kwargs)



    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= self.auction.current_bid:
            raise forms.ValidationError('Your bid must be higher than the current highest bid.')
        return amount


class CommentForm:
    class Meta:
        model = Comment
        fields = ['auction', 'content']

        def __init__(self, *args, **kwargs):
            self.auction = kwargs.pop('auction', None)
            super().__init__(*args, **kwargs)

