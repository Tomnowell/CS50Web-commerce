from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime, timedelta, timezone


class User(AbstractUser):
    def __str__(self):
        return str(self.username)


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
        choices=CATEGORIES, default="Home", max_length=255, blank=False)
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_bids = models.IntegerField(default=0)
    picture_link = models.URLField(null=True)
    start_time = models.DateTimeField(
        default=datetime.now(timezone.utc), editable=False)
    end_time = models.DateTimeField(
        default=(datetime.now(timezone.utc) + timedelta(7)))

    def increment_bid_number(self):
        self.number_of_bids += 1

    def __str__(self):
        return f"Listing: {str(self.name)} Owner: {str(self.auctioneer.username)} Start: {str(self.start_time)} End: {str(self.end_time)}"

    def __eq__(self, other):
        return self.auctioneer == other.auctioneer


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now=True)

<<<<<<< HEAD
    def get_current_bid(item, bid):
        """[Returns the current bid]

        Args:
            item ([Listing]): [The Listing details as a Listing model]
            bid ([Bid]): [the current high bid, could be replaced by this bid]
        """

    def __eq__(self, Bid):
        if self.amount == Bid.amount:
=======
    def __eq__(self, bid):
        if self.amount == bid.amount:
>>>>>>> 6fd315f7ac67c1b96dcf0f29b9fab6ed83c1e017
            return True
        return False

    def __str__(self):
        return f"{str(self.bidder.username)}->{str(self.item.name)}->{str(self.amount)}"

    def get_current_bid(self):
        bid_list = self.get_all_bids(self)
        current_bid = 0
        for bid in bid_list:
            if bid.amount > current_bid:
                current_bid = bid.amount
        return(current_bid)

    def get_all_bids(item):
        bids = Bid.objects.filter(item=item)
        return bids


class Comment(models.Model):
    commentor = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="commented_listing")
    comment = models.TextField(blank=True, max_length=1024)
    votes = models.IntegerField()

    def __str__(self):
        return f"{str(self.commentor.username)}->{str(self.comment)}->votes:{str(self.votes)}"


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
    stars = models.IntegerField()
