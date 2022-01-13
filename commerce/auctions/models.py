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
    picture_link = models.URLField(null=True)

    def __str__(self):
        return f"{self.name}:{self.current_top_bid}"


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
    comment = models.TextField(blank=True)
    votes = models.DecimalField(max_digits=6)

    def __str__(self):
        return f"{self.commentor}->{self.comment}->votes:{self.votes}"
