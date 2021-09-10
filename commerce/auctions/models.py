from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=128)
    host = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    current_top_bid = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_bids = models.IntegerField(blank=True)
    picture_link = models.URLField(null=True)

    def __str__(self):
        return f"{self.name}:{self.current_top_bid}"


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="item_bids")
    item = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)

    def __eq__(self, Bid):
        if self.amount == Bid.amount:
            return True
        return False

    def __str__(self):
        return f"{self.bidder}->{self.item}->{self.amount}"
