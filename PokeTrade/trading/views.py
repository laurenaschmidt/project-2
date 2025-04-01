from django.shortcuts import render, get_object_or_404

from .models import Pokemon, Collection, Trade, Sale, WishList, Favorite, Leaderboard, UserProfile, LeaderboardEntry, \
    Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .utils import fetch_pokemon


@login_required
def home(request):
    pokemons_for_sale = Sale.objects.all()
    context = {'pokemons_for_sale': pokemons_for_sale}
    return render(request, 'trading/home.html')


@login_required
def pokemon_list(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'trading/pokemon_list.html', {'pokemons': pokemons})

def pokemon_detail(request, pokemon_name):
    pokemon_data = fetch_pokemon(pokemon_name)
    return render(request, 'trading/pokemon_detail.html', {'pokemon': pokemon_data})

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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    leaderboard_entries = LeaderboardEntry.objects.all().order_by('-score')
    return render(request, 'trading/leaderboard.html', {'leaderboard_entries': leaderboard_entries})

def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    collection = user_profile.collection.all()
    wishlist = user_profile.wishlist.all()
    favorites = user_profile.favorites.all()

    context = {
        'user_profile': user_profile,
        'collection': collection,
        'wishlist': wishlist,
        'favorites': favorites,
    }
    return render(request, 'trading/profile.html', context)


def trade(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Get trades where the user is either the sender or the receiver
    user_trades = Trade.objects.filter(sender=user_profile) | Trade.objects.filter(receiver=user_profile)

    return render(request, 'trading/trade.html', {'trades': user_trades})


def sale(request):
    pokemons_for_sale = Sale.objects.all()
    context = {'pokemons_for_sale': pokemons_for_sale}
    return render(request, 'trading/sale.html')

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    context = {'user_notifications': user_notifications}
    return render(request, 'trading/notifications.html')


def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_trades = Trade.objects.filter(sender=user_profile) | Trade.objects.filter(receiver=user_profile)

    context = {
        'user_profile': user_profile,
        'user_trades': user_trades,
    }
    return render(request, 'trading/profile.html', context)


def trade_list(request):
    # Display a list of trades, can be filtered or sorted as needed
    trades = Trade.objects.all()
    context = {
        'trades': trades
    }
    return render(request, 'trading/trade_list.html', context)
