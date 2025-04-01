from django.db import models
from django.contrib.auth.models import User

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pokemon_images/', null=True, blank=True)

    def __str__(self):
        return self.name
class Collection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pokemon = models.ManyToManyField(Pokemon, related_name='collections')


class Trade(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_trades')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_trades')
    pokemon_offered = models.ManyToManyField(Pokemon, related_name='offered_in_trades')
    pokemon_requested = models.ManyToManyField(Pokemon, related_name='requested_in_trades')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)


class Sale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pokemon = models.ManyToManyField(Pokemon, related_name='wishlisted_by')


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Analytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.JSONField()

