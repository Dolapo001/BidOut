from django.db import models
from autoslug import AutoSlugField
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from users.models import User
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    start_date = models.DateTimeField(auto_now_add=True)
    place_bid = models.OneToOneField('Bid', blank=True, related_name='bids', on_delete=models.CASCADE, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    end_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='winner_auctions')
    is_closed = models.BooleanField(default=False)

    def close_auction(self):
        if not self.is_closed:
            highest_bid = Bid.objects.filter(auction=self).order_by('-bid_amount').first()
            if highest_bid:
                self.highest_bidder = highest_bid.bidder
            self.is_closed = True
            self.save()

    def __str__(self):
        return self.title


    @staticmethod
    def label_from_instance(instance):
        return instance.name


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid for {self.auction.title} by {self.bidder.username} - ${self.amount}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.auction.title} by {self.user.username}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.auction.title}"
