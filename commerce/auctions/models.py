from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime, timedelta, timezone

from decimal import Decimal


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    CATEGORIES = [
        ("AUTOMOTIVE", "Automotive"),
        ("ELCTRONICS", "Electronics & Computers"),
        ("FASHION", "Fashion"),
        ("GARDEN", "Garden"),
        ("HOME", "Home"),
        ("INDUSTRIAL", "Industrial"),
        ("MANGA", "Japanese manga & anime"),
        ("LIFESTYLE", "Lifestyle"),
        ("MUSIC", "Music & Musical Instruments"),
        ("SPORTS", "Sports"),
        ("SOFTWARE", "Software & Computer Games"),
        ("SPACESHIPS", "Spaceships")
    ]

    name = models.CharField(max_length=64)
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        choices=CATEGORIES, default="HOME", max_length=128, blank=False)
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_bids = models.IntegerField(default=0)
    picture_link = models.URLField(null=True)
    start_time = models.DateTimeField(
        default=datetime.now(timezone.utc), editable=False)
    end_time = models.DateTimeField(
        default=(datetime.now(timezone.utc) + timedelta(7)))
    open = models.BooleanField(default=True)

    watchlist = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlist")

    def increment_bid_count(self):
        self.number_of_bids += 1
        self.save()

    def close_listing(self):
        self.open = False
        self.save()

    def is_listing_expired(self):
        if datetime.now(timezone.utc) > self.end_time:
            self.close_listing()
            self.save()
        return self.open

    def get_current_bid(self):
        """
        [returns: current highest bid (Bid object)]
        """
        bid_list = self.get_all_bids()
        try:
            return max(bid_list)
        except ValueError:
            return None

    def get_bid_count(self):
        return self.number_of_bids

    def get_all_bids(self):
        return Bid.objects.filter(item=self)

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(
        default=datetime.now(timezone.utc), editable=False)

    def __ne__(self, other):
        return self.amount != other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __ge__(self, other):
        return self.amount >= other.amount

    def __str__(self):
        return f"{self.bidder.username} -> {self.item.name} -> {self.amount}"


class Comment(models.Model):
    commentor = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, max_length=1024)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commentor.username} -> {self.item} -> {self.comment}"
