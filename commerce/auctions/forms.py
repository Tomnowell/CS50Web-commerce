from cProfile import label
from unicodedata import category
from django.forms import ModelForm
from .models import Listing, Bid, Comment, Review


class listing_form(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'auctioneer', 'category', 'description',
                  'starting_bid', 'picture_link', 'start_time', 'end_time']
