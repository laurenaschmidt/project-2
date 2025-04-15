from django.db import models
from django.contrib.auth.models import User



class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)# Store as a comma-separated string
    image = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    favorite_pokemon = models.ForeignKey(Pokemon, on_delete=models.SET_NULL, null=True, blank=True, related_name='favorited_by')
    collection = models.ManyToManyField(Pokemon, related_name='collected_by', blank=True)
    owned_pokemon = models.ManyToManyField(Pokemon, blank=True)

    def __str__(self):
        return self.user.username


class Collection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pokemon = models.ManyToManyField(Pokemon, related_name='collections')



class Trade(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_trades', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_trades', on_delete=models.CASCADE)
    pokemon_offered = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='trades_offered', null=True, blank=True)
    pokemon_requested = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='trades_requested', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)


class Sale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pokemon.name} - ${self.price}"

class WishList(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    pokemon = models.ManyToManyField(Pokemon, related_name='wishlisted_by')

    def __str__(self):
        return f"{self.user.user.username}'s Wishlist"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pokemon')


class TradeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)


class Release(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Analytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.JSONField()

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='leaderboard_entries')
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.user.username} - {self.score}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pokemon')

    def __str__(self):
        return f"{self.user.username} - {self.pokemon.name}"

class ForSale(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    listed_at = models.DateTimeField(auto_now_add=True)
