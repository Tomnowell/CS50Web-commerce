from cProfile import label
from unicodedata import category
from django.forms import ModelForm
from .models import Listing, Bid, Comment


class listing_form(ModelForm):
    class Meta:
        model = Listing
        fields = ['name',  'category', 'description',
                  'starting_bid', 'picture_link', 'end_time']


class bid_form(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


class comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
