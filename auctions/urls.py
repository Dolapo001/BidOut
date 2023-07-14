from django.urls import path
from . import views
from .views import watchlist, add_to_watchlist, remove_from_watchlist, category_list, category_auctions, auction

urlpatterns = [
    path('', views.home, name="home"),
    path('active-auctions', views.auctions, name="auctions"),
    path('auction/<uuid:pk>/', auction, name='auction'),
    path('auctions/<uuid:pk>/', views.auction, name='auction_detail'),
    path('create-auction', views.createAuction, name="create-auction"),
    path('place-bid/<uuid:pk>/', views.auction, name="place-bid"),
    path('categories/', category_list, name='categories'),
    path('categories/<slug:slug>/', category_auctions, name='category_auctions'),
    path('watchlist/', watchlist, name='watchlist'),
    path('auction/<int:auction_id>/add_watchlist/', views.add_to_watchlist, name='add_watchlist'),
    path('auction/<int:auction_id>/remove_watchlist/', views.remove_from_watchlist, name='remove_watchlist'),
]

