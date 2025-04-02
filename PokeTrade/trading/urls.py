from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'trading'

urlpatterns = [
    path('', views.home, name='home'),
    path('pokemons/', views.pokemon_list, name='pokemon_list'),
    path('collection/', views.user_collection, name='user_collection'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('trade/', views.trade, name='trade'),
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
]