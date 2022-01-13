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
    CATEGORIES = [
        "Automotive",
        "Electronics & Computers",
        "Fashion",
        "Garden",
        "Home",
        "Industrial",
        "Japanese manga & anime",
        "Lifestyle",
        "Music & Musical Instruments",
        "Sports",
        "Software & Computer Games",
        "Spaceships"
    ]

    name = models.CharField(max_length=128)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(choices=CATEGORIES, default="Automotive")
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    picture_link = models.URLField(null=True)
    self.start_time = models.DateTimeField
    self.end_time = models.DateTimeField

    def __str__(self):
        return f"Listing: {self.name} Owner: {self.owner} Top Bid:{self.current_top_bid}"

    def save(self):
        self.starting_time = datetime(now)
        self.ending_time = (self.starting_time + 7)


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="item_bidder")
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_on_item")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)

    def __eq__(self, Bid):
        if self.amount == Bid.amount:
            return True
        return False

    def __str__(self):
        return f"{self.bidder}->{self.item}->{self.amount}"


class Comment(models.Model):
    commentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commentor")
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="commented_listing")
    comment = models.TextField(blank=True, max_length=1024)
    votes = models.IntegerField(max_digits=6)

    def __str__(self):
        return f"{self.commentor}->{self.comment}->votes:{self.votes}"
        return f"Bidder: {self.bidder} Item: {self.item} Bid: {self.amount}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist")


class Review(models.Model):
    review = models.TextField(max_length=1024)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(max_length=1)
