from django.shortcuts import render

from .models import Pokemon, Collection, Trade, Sale, WishList, Favorite, Leaderboard
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def home(request):
    return render(request, 'trading/home.html')


@login_required
def pokemon_list(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'trading/pokemon_list.html', {'pokemons': pokemons})


@login_required
def user_collection(request):
    collection = Collection.objects.get(user=request.user)
    return render(request, 'trading/collection.html', {'collection': collection})


@login_required
def wishlist(request):
    wishlist = WishList.objects.get(user=request.user)
    return render(request, 'trading/wishlist.html', {'wishlist': wishlist})


@login_required
def leaderboard(request):
    leaders = Leaderboard.objects.order_by('-score')[:5]
    return render(request, 'trading/leaderboard.html', {'leaders': leaders})

def profile(request):
    return render(request, 'trading/profile.html')

def trade(request):
    return render(request, 'trading/trade.html')

def sale(request):
    return render(request, 'trading/sale.html')

def notifications(request):
    return render(request, 'trading/notifications.html')
