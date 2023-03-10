from django.urls import path
from . import views

urlpatterns = [
    path('', views.auctions, name="auctions"),
    path('auction/<str:pk>/', views.auction, name="auction"),

]
