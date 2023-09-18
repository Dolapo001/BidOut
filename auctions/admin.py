from django.contrib import admin

# Register your models here.
from .models import Auction, Bid, Comment, Category

admin.site.register([
    Auction,
    Bid,
    Comment,
    Category
])
