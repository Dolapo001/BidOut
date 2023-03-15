from django.urls import path
from . import views

urlpatterns = [
    path('', views.auctions, name="auctions"),
    path('auction/<str:pk>/', views.auction, name="auction"),
    path('create-auction', views.createAuction, name="create-auction"),
    path('place-bid/<str:pk>/', views.placeBid, name="place-bid"),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category>/', views.auctionCategory, name='auction-category'),

 ]
