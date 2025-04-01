from django.contrib import admin

from .models import (
    Pokemon, Collection, Trade, Sale, WishList,
    Favorite, TradeHistory, Release, Leaderboard,
    Notification, Analytics
)

admin.site.register(Pokemon)
admin.site.register(Collection)
admin.site.register(Trade)
admin.site.register(Sale)
admin.site.register(WishList)
admin.site.register(Favorite)
admin.site.register(TradeHistory)
admin.site.register(Release)
admin.site.register(Leaderboard)
admin.site.register(Notification)
admin.site.register(Analytics)
