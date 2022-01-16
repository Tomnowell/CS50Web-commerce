from cProfile import label
from unicodedata import category
from django.forms import *
from .models import Listing, Bid, Comment, Review


class listing_form(ModelForm):
    name = CharField(label="Name", required=True, widget=TextInput())
    category = ChoiceField(required=True, choices=Listing.CATEGORIES)
    description = CharField(label="Description")
    picture_link = URLField(label="Picture URL")
    starting_bid = DecimalField(decimal_places=2)
    end_date = DateField()
