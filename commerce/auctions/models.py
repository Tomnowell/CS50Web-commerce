from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timezone

CATEGORIES = [
    "Accessories",
    "Household & Bathroom",
    "DIY",
    "Electronics",
    "Specialist",
    "Computers & Consoles",
    "Clothing",
    "Food & Perishables",
    "Booze"

]


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")

    description = models.TextField(max_length=1000)
    start_time = models.DateTimeField()
    start_bid = models.DecimalField(
        max_digits=8,
        decimal_places=2)
    end_time = models.DateTimeField()
    image_link = models.URLField(null=True)
    category = models.CharField(choices=CATEGORIES)

    bids = models.ForeignKey(
        Bid, on_delete=models.DO_NOTHING, related_name="bids")

    def __str__(self):
        return f"Listing: {self.name} Owner: {self.owner} Top Bid:{self.current_top_bid}"

    def save(self, *args, **kwargs):
        self.starting_time = datetime(now)
        self.ending_time = (self.starting_time + 7)


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)

    def __eq__(self, Bid):
        if self.amount == Bid.amount:
            return True
        return False

    def __str__(self):
        return f"Bidder: {self.bidder} Item: {self.item} Bid: {self.amount}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist")


class Review(models.Model):
    review = models.TextField(max_length=1024)
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True)
