from django.urls import path
from . import views
from .views import watchlist, add_to_watchlist, remove_from_watchlist, category_list, category_auctions

urlpatterns = [
    path('', views.home, name="home"),
    path('active-auctions', views.auctions, name="auctions"),
    path('auction/<str:pk>/', views.auction, name="auction"),
    path('auctions/<uuid:pk>/', views.auction, name='auction_detail'),
    path('create-auction', views.createAuction, name="create-auction"),
    path('place-bid/<str:pk>/', views.placeBid, name="place-bid"),
    path('categories/', category_list, name='categories'),
    path('categories/<slug:slug>/', category_auctions, name='category_auctions'),
    path('watchlist/', watchlist, name='watchlist'),
    path('add-to-watchlist/<str:pk>/', add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<str:pk>/', remove_from_watchlist, name='remove_from_watchlist'),
]
