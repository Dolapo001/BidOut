from django.contrib.auth.models import User
from django.contrib.postgres import serializers
from django.db import models
from autoslug import AutoSlugField
import uuid


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True)
    slug = AutoSlugField(populate_from="name", always_update=True, unique=True, default='')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None, related_name="auctions")
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @staticmethod
    def label_from_instance(instance):
        return instance.name


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.auction.title}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.auction.title} by {self.user.username}"



