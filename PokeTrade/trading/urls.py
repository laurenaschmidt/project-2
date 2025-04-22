from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'trading'

urlpatterns = [
    path('', views.home, name='home'),

    # Pokemon + Profile
    path('pokemons/', views.pokemon_list, name='pokemon_list'),
    path('pokemon/<str:pokemon_name>/', views.pokemon_detail, name='pokemon_detail'),
    path('collection/', views.user_collection, name='user_collection'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/<str:username>/', views.view_user_profile, name='view_user_profile'),
    path('collection/', views.full_collection, name='full_collection'),

    # Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),
    path('favorite/<int:pokemon_id>/', views.favorite_pokemon, name='favorite_pokemon'),
    path('buy/<int:pokemon_id>/', views.buy_pokemon, name='buy_pokemon'),
    path('release/<int:pokemon_id>/', views.release_pokemon, name='release_pokemon'),
    path('list_for_sale/<int:pokemon_id>/', views.list_pokemon_for_sale, name='list_pokemon_for_sale'),

    # Trades
    path('trades/', views.trade_list, name='trade_list'),
    path('create_trade/', views.create_trade, name='create_trade'),
    path('create_trade/<int:pokemon_offered_id>/<int:receiver_id>/<int:pokemon_requested_id>/', views.create_trade,
         name='create_trade'),
    path('accept_trade/<int:trade_id>/', views.accept_trade, name='accept_trade'),
    path('reject_trade/<int:trade_id>/', views.reject_trade, name='reject_trade'),
    path('trade_offers/', views.trade_offers_view, name='trade_offers'),

    # Leaderboard, Sale, Notifications, Wishlist
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('sale/', views.sale, name='sale'),
    path('notifications/', views.notifications, name='notifications'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:pokemon_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),


    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='trading/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # API
    path('api/get_user_pokemon/<int:user_id>/', views.get_user_pokemon, name='get_user_pokemon'),
    path('import/<str:pokemon_name>/', views.import_pokemon, name='import_pokemon'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)