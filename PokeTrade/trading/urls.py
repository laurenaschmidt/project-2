from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pokemons/', views.pokemon_list, name='pokemon_list'),
    path('collection/', views.user_collection, name='user_collection'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]