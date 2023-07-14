from django.urls import path
from . import views
from .views import watchlist, add_to_watchlist, remove_from_watchlist, category_list, category_auctions, auction

urlpatterns = [
    path('', views.home, name="home"),
    path('active-auctions', views.auctions, name="auctions"),
    path('auction/<uuid:pk>/', views.auction, name='auction'),
    path('auctions/<uuid:pk>/', views.auction, name='auction_detail'),
    path('create-auction', views.createAuction, name="create-auction"),
    path('place-bid/<uuid:pk>/', views.auction, name="place-bid"),
    path('categories/', category_list, name='categories'),
    path('auction/close/<uuid:pk>/', views.close_auction, name='close_auction'),
    path('categories/<slug:slug>/', category_auctions, name='category_auctions'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add-to-watchlist/<uuid:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<uuid:pk>/', views.remove_from_watchlist, name='remove_from_watchlist'),

]
