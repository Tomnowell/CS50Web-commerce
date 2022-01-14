from django.contrib import admin
from .models import Listing, User, Bid, Comment, Watchlist, Review

# Register your models here.
# admin.site.register(modelname)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Review)
