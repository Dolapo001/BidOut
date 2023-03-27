from django.urls import path
from . import views
from .views import watchlist, add_to_watchlist, remove_from_watchlist

urlpatterns = [
    path('', views.home, name="home"),
    path('active-auctions', views.auctions, name="auctions"),
    path('auction/<str:pk>/', views.auction, name="auction"),
    path('create-auction', views.createAuction, name="create-auction"),
    path('place-bid/<str:pk>/', views.placeBid, name="place-bid"),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category>/', views.auctionCategory, name='auction-category'),
    path('watchlist/', watchlist, name='watchlist'),
    path('add-to-watchlist/<str:pk>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<str:pk>/', remove_from_watchlist, name='remove_from_watchlist'),
]
