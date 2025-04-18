from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'trading'

urlpatterns = [
    path('', views.home, name='home'),
    path('pokemons/', views.pokemon_list, name='pokemon_list'),
    path('collection/', views.user_collection, name='user_collection'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('sale/', views.sale, name='sale'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('trades/', views.trade_list, name='trade_list'),
    path('import/<str:pokemon_name>/', views.import_pokemon, name='import_pokemon'),
    path('pokemon/<str:pokemon_name>/', views.pokemon_detail, name='pokemon_detail'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='trading/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('favorite/<int:pokemon_id>/', views.favorite_pokemon, name='favorite_pokemon'),
    path('buy/<int:pokemon_id>/', views.buy_pokemon, name='buy_pokemon'),
    path('release/<int:pokemon_id>/', views.release_pokemon, name='release_pokemon'),
    path('trade/', views.trade_list, name='trade_list'),
    path('create_trade/', views.create_trade, name='create_trade'),
    path('accept_trade/<int:trade_id>/', views.accept_trade, name='accept_trade'),
    path('profile/<str:username>/', views.view_user_profile, name='view_user_profile'),
    path('list_for_sale/<int:pokemon_id>/', views.list_pokemon_for_sale, name='list_pokemon_for_sale'),
    path('api/get_user_pokemon/<int:user_id>/', views.get_user_pokemon, name='get_user_pokemon'),
    path('reject_trade/<int:trade_id>/', views.reject_trade, name='reject_trade'),
    path('create_trade/<int:pokemon_offered_id>/<int:receiver_id>/<int:pokemon_requested_id>/', views.create_trade, name='create_trade'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)