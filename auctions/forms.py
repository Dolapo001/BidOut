from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets
from django import forms
from .models import Auction, Bid, Comment


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'featured_image', 'description', 'price', 'starting_bid', 'category']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bid amount',
                'min': '0.01',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction', None)
        super(BidForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

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



