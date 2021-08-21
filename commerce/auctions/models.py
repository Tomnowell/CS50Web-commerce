from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    current_top_bid = models.DecimalField(max_digits=8, decimal_places=2)
    bids = models.IntegerField(blank=True)
    picture_link = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.name}:{self.current_top_bid}"
