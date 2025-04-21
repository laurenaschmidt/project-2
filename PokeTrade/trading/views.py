import random
from collections import Counter

from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from . import models
from .forms import UserProfileForm, CustomSignupForm
from .models import Pokemon, Collection, Trade, Sale, WishList, Favorite, Leaderboard, UserProfile, LeaderboardEntry, \
    Notification, ForSale
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .utils import fetch_pokemon


@login_required
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

def leaderboard(request):
    top_users = UserProfile.objects.annotate(
        num_pokemon=Count('owned_pokemon')).order_by('-num_pokemon')

    return render(request, 'trading/leaderboard.html', {'top_users': top_users})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorites = Favorite.objects.filter(user=request.user).select_related('pokemon')
    owned_pokemon = user_profile.owned_pokemon.all()
    type_counts = Counter(pokemon.type for pokemon in owned_pokemon)
    total_owned = owned_pokemon.count()
    unique_types = len(type_counts)
    most_common_type = type_counts.most_common(1)[0][0] if type_counts else None
    type_percentages = {
        t: (count / total_owned) * 100 for t, count in type_counts.items()
    } if total_owned else {}
    context = {'user_profile': user_profile, 'type_percentages': type_percentages,
        'most_common_type': most_common_type,
        'total_owned': total_owned,
        'unique_types': unique_types,
        'favorites': favorites,}
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

@login_required
def marketplace(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    search_query = request.GET.get('search', '')
    if search_query:
        pokemon_list = Pokemon.objects.filter(
            Q(name__icontains=search_query) |
            Q(type__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    else:
        pokemon_list = Pokemon.objects.all()

    sales = ForSale.objects.select_related('pokemon', 'seller').all()

    context = {
        'pokemon_list': pokemon_list,
        'sales': sales,
        'user_profile': user_profile,
    }

    return render(request, 'trading/marketplace.html', context)

@login_required
def trade(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_trades = Trade.objects.filter(sender=user_profile) | Trade.objects.filter(receiver=user_profile)

    return render(request, 'trading/trade.html', {'trades': user_trades})


def sale(request):
    pokemons_for_sale = Sale.objects.all()
    context = {'pokemons_for_sale': pokemons_for_sale}
    return render(request, 'trading/sale.html')

@login_required
def notifications(request):
    user_profile = UserProfile.objects.get(user=request.user)
    notifications = user_profile.notifications.order_by('-timestamp')
    return render(request, 'trading/notifications.html', {'notifications': notifications})


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
        user_profile = get_object_or_404(UserProfile, user=request.user)
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
        Favorite.objects.create(user=request.user, pokemon=pokemon)
        user_profile.favorite_pokemon = pokemon
        user_profile.save()
        return redirect('trading:profile')


@login_required
def buy_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    user_profile = UserProfile.objects.get(user=request.user)

    try:
        # Check if the Pokémon is being sold by another user
        sale = ForSale.objects.get(pokemon=pokemon)

        # Remove Pokémon from the seller's owned list
        seller_profile = sale.seller
        seller_profile.owned_pokemon.remove(pokemon)
        seller_profile.save()
        sale.delete()

    except ForSale.DoesNotExist:
        pass

    user_profile.owned_pokemon.add(pokemon)
    user_profile.save()

    return redirect('trading:marketplace')

def release_pokemon(request, pokemon_id):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
        user_profile.owned_pokemon.remove(pokemon)
        return redirect('trading:profile')
    else:
        return redirect('trading:profile')

@login_required
def trade_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_trades = Trade.objects.filter(sender=user_profile)
    available_trades = Trade.objects.filter(receiver=user_profile, accepted=False)
    other_users = UserProfile.objects.exclude(user=request.user)

    user_ids = Trade.objects.filter(
        accepted=False,
        receiver=user_profile
    ).values_list("sender", flat=True).distinct()
    users_with_trades = UserProfile.objects.filter(id__in=user_ids)

    context = {
        'user_profile': user_profile,
        'user_trades': user_trades,
        'available_trades': available_trades,
        'other_users': other_users,
        'other_users_with_trades_to_me': users_with_trades
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        receiver_id = request.POST.get('receiver_id')
        pokemon_offered_id = request.POST.get('pokemon_offered_id')
        pokemon_requested_id = request.POST.get('pokemon_requested_id')

        if receiver_id and pokemon_offered_id and pokemon_requested_id:
            try:
                receiver_profile = UserProfile.objects.get(id=receiver_id)
                selected_offered = Pokemon.objects.get(id=pokemon_offered_id)
                selected_requested = Pokemon.objects.get(id=pokemon_requested_id)

                context.update({
                    'selected_offered': selected_offered,
                    'selected_requested': selected_requested,
                    'receiver_profile': receiver_profile,
                })
            except (UserProfile.DoesNotExist, Pokemon.DoesNotExist):
                pass

            if action == 'compare':
                # Just render the comparison view with context
                return render(request, 'trading/trade_list.html', context)

            elif action == 'submit':
                # Redirect to the create_trade view, passing Pokémon IDs via URL
                return redirect('trading:create_trade', pokemon_offered_id=selected_offered.id, receiver_id=receiver_profile.id, pokemon_requested_id=selected_requested.id)

        return render(request, 'trading/trade_list.html', context)

    return render(request, 'trading/trade_list.html', context)


from django.shortcuts import get_object_or_404, redirect
from .models import UserProfile, Pokemon, Trade, Notification


def create_trade(request, pokemon_offered_id, receiver_id, pokemon_requested_id):
    sender_profile = UserProfile.objects.get(user=request.user)
    receiver_profile = get_object_or_404(UserProfile, id=receiver_id)
    pokemon_offered = get_object_or_404(Pokemon, id=pokemon_offered_id)
    pokemon_requested = get_object_or_404(Pokemon, id=pokemon_requested_id)

    # Check if trade already exists? Optional.
    Trade.objects.create(
        sender=sender_profile,
        receiver=receiver_profile,
        pokemon_offered=pokemon_offered,
        pokemon_requested=pokemon_requested,
    )

    # Create a notification
    Notification.objects.create(
        user=receiver_profile,
        message=f"You received a trade offer from {request.user.username}: {pokemon_offered.name} for {pokemon_requested.name}"
    )

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



def view_user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    pokemon_for_sale = ForSale.objects.filter(seller=user_profile)
    trades_sent = Trade.objects.filter(sender=user_profile)
    trades_received = Trade.objects.filter(receiver=user_profile)
    favorites = Favorite.objects.filter(user=user).select_related('pokemon')
    return render(request, 'trading/view_user_profile.html', {'user_profile': user_profile, 'favorites': favorites, 'pokemon_for_sale': pokemon_for_sale, 'trades_sent': trades_sent, 'trades_received': trades_received})

@login_required
def list_pokemon_for_sale(request, pokemon_id):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)

        if pokemon in user_profile.owned_pokemon.all():
            price = request.POST.get('price')
            ForSale.objects.create(seller=user_profile, pokemon=pokemon, price=price)
            return redirect('trading:profile')

    return redirect('trading:profile')

def get_user_pokemon(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    pokemon = profile.owned_pokemon.all()
    data = {
        'pokemon': [{'id': p.id, 'name': p.name} for p in pokemon]
    }
    return JsonResponse(data)

@require_POST
def reject_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    if trade.receiver.user == request.user:
        trade.delete()
        messages.success(request, "Trade rejected.")
    else:
        messages.error(request, "You are not authorized to reject this trade.")

    return redirect('trading:trade_list')

@login_required
def wishlist_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    wishlist, created = WishList.objects.get_or_create(user=user_profile)
    all_pokemon = Pokemon.objects.all()

    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        if pokemon_id:
            pokemon = get_object_or_404(Pokemon, id=pokemon_id)
            wishlist.pokemon.add(pokemon)
            wishlist.save()
            return redirect('trading:wishlist')

    context = {
        'wishlist': wishlist,
        'all_pokemon': all_pokemon,
    }

    return render(request, 'trading/wishlist_view.html', context)

@login_required
def trade_offers_view(request, trade_id=None):  
    print("TRADE OFFERS VIEW")
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)  
    trades = Trade.objects.filter(receiver=user_profile, accepted=False)
    user_id = request.GET.get("user")

    if user_id:
        try:
            user_id = int(user_id)
            trades = trades.filter(sender__id=user_id, receiver=user_profile)
        except ValueError:
            pass 

    user_ids = Trade.objects.filter(
        accepted=False,
        receiver=user_profile
    ).values_list("sender", flat=True).distinct()
    users_with_trades = UserProfile.objects.filter(id__in=user_ids)

    context = {
        "available_trades": trades,
        "other_users_with_trades_to_me": users_with_trades,
        "user_profile": user_profile,
    }
    return render(request, "trading/trade_list.html", context)

