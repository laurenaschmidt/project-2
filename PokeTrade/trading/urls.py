from django.urls import path
from . import views

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
]