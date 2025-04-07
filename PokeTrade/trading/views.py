import random

from django.contrib.auth import login
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserProfileForm, CustomSignupForm
from .models import Pokemon, Collection, Trade, Sale, WishList, Favorite, Leaderboard, UserProfile, LeaderboardEntry, \
    Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .utils import fetch_pokemon


@login_required(login_url='/signup')
def home(request):
    pokemons_for_sale = Sale.objects.all()
    context = {'pokemons_for_sale': pokemons_for_sale}
    return render(request, 'trading/home.html')


def import_pokemon(request, pokemon_name):
    data = fetch_pokemon(pokemon_name)

    if data:
        pokemon, created = Pokemon.objects.get_or_create(
            name=data['name'].capitalize(),
            number=data['id'],
            type=', '.join([t['type']['name'].capitalize() for t in data['types']]),
            image=data['sprites']['front_default'] if data['sprites']['front_default'] else None
        )
        if created:
            pokemon.save()
        return redirect('pokemon_detail', pokemon_name=pokemon_name)
    else:
        return render(request, 'trading/error.html', {'message': 'Pokemon not found'})

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


def leaderboard(request):
    top_users = UserProfile.objects.annotate(
        num_pokemon=Count('owned_pokemon')).order_by('-num_pokemon')[:5]

    return render(request, 'trading/leaderboard.html', {'top_users': top_users})

@login_required(login_url='/signup')
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'trading/profile.html', context)


@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('trading:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'trading/update_profile.html', {'form': form})

def marketplace(request):
    pokemon_list = Pokemon.objects.all()  # Make sure you have Pokemon objects in your database!
    context = {'pokemon_list': pokemon_list,}
    available_sales = Sale.objects.filter(available=True)
    return render(request, 'trading/marketplace.html', context)

@login_required(login_url='/signup')
def trade(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_trades = Trade.objects.filter(sender=user_profile) | Trade.objects.filter(receiver=user_profile)

    return render(request, 'trading/trade.html', {'trades': user_trades})


def sale(request):
    pokemons_for_sale = Sale.objects.all()
    context = {'pokemons_for_sale': pokemons_for_sale}
    return render(request, 'trading/sale.html')

@login_required(login_url='/signup')
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


def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            all_pokemon = list(Pokemon.objects.all())
            random_pokemon = random.sample(all_pokemon, k=min(3, len(all_pokemon)))

            for p in random_pokemon:
                user_profile.owned_pokemon.add(p)

            user_profile.save()
            return redirect('trading:marketplace')
    else:
        form = CustomSignupForm()
    return render(request, 'trading/signup.html', {'form': form})


def favorite_pokemon(request, pokemon_id):
    if request.method == "POST":
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, pokemon=pokemon)
        if not created:
            favorite.delete()
    return redirect('trading:marketplace')


@login_required
def buy_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    user_profile = UserProfile.objects.get(user=request.user)

    # Add the Pokémon to the user's owned Pokémon
    user_profile.owned_pokemon.add(pokemon)
    user_profile.save()

    return redirect('trading:marketplace')

def remove_pokemon(request, pokemon_id):
    if not request.user.is_authenticated:
            return redirect('login')
            print("🔍 remove_pokemon view called!")
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
        user_profile.owned_pokemon.remove(pokemon)
        return redirect('trading:profile')
    else:
        return redirect('trading:profile')

@login_required
def trade_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_trades = Trade.objects.filter(sender=user_profile) | Trade.objects.filter(receiver=user_profile)
    available_trades = Trade.objects.exclude(sender=user_profile)

    other_users = UserProfile.objects.exclude(id=user_profile.id)

    return render(request, 'trading/trade_list.html', {
        'user_trades': user_trades,
        'available_trades': available_trades,
        'user_profile': user_profile,
        'other_users': other_users,
    })


def create_trade(request):
    if request.method == 'POST':
        sender = get_object_or_404(UserProfile, user=request.user)
        receiver = get_object_or_404(UserProfile, id=request.POST.get('receiver_id'))
        offered = get_object_or_404(Pokemon, id=request.POST.get('pokemon_offered_id'))
        requested_name = request.POST.get('pokemon_requested_name')
        requested = get_object_or_404(Pokemon, name__iexact=requested_name)

        trade = Trade.objects.create(
            sender=sender,
            receiver=receiver,
            pokemon_offered=offered,
            pokemon_requested=requested
        )
        return redirect('trading:trade_list')

    return redirect('trading:trade_list')


@login_required
def accept_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    if trade.receiver.user == request.user and not trade.accepted:
        trade.receiver.owned_pokemon.remove(trade.pokemon_requested)
        trade.sender.owned_pokemon.remove(trade.pokemon_offered)

        trade.receiver.owned_pokemon.add(trade.pokemon_offered)
        trade.sender.owned_pokemon.add(trade.pokemon_requested)

        trade.accepted = True
        trade.save()
    return redirect('trading:trade_list')
