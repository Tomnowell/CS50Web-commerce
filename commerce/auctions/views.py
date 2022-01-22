from asyncio import exceptions
from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal

from .models import *
from .forms import *


def index(request):
    listings = Listing.objects.all()
    return main_view(request, listings)


def main_view(request, listings):
    return render(request, "auctions/index.html", {
        'listings': listings,
        "categories": Listing.CATEGORIES
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def show_entries(request):
    if request.method == "GET":
        # Show all entries
        return render(request, "auctions/listings.html", {
            'listings': Listing.objects.all()
        })


def is_user_also_auctioneer(request, listing):
    if request.user.username == listing.auctioneer:
        return True
    return False


def show_listing(request, id):
    if request.method == "GET":
        return show_listing_GET(request, id)
    elif request.method == "POST":
        return show_listing_POST(request, id)
    else:
        return show_listing_GET(request, id)


def show_listing_GET(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)

    end_button_visibility = "disabled"
    aria_disabled = "true"
    tab_index = "-1"

    if is_user_also_auctioneer(request, current_listing):
        end_button_visibility = "active"
        aria_disabled = "false"
        tab_index = "1"

    return render(request, "auctions/listing.html", {"listing": current_listing,
                                                     "visibility": end_button_visibility,
                                                     "aria_dissabled": aria_disabled,
                                                     "tab_index": tab_index})


def show_listing_POST(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {"listing": current_listing})


def create(request):
    if request.method == "GET":
        return create_if_GET(request)

    elif request.method == "POST":
        return create_if_POST(request)

    else:
        return create_if_GET(request)


def create_if_GET(request):
    form = listing_form()
    return render(request, "auctions/create.html", {"form": form})


@login_required(login_url="/login")
def create_if_POST(request):
    form = listing_form(request.POST)

    if form.is_valid():
        new_listing = Listing()
        new_listing.name = form.cleaned_data['name']
        new_listing.auctioneer = request.user
        new_listing.category = form.cleaned_data['category']
        new_listing.description = form.cleaned_data['description']
        new_listing.starting_bid = form.cleaned_data['starting_bid']
        new_listing.picture_link = form.cleaned_data['picture_link']
        new_listing.end_time = form.cleaned_data['end_time']
        new_listing.save()
        new_listing_id = str(new_listing.id)
        return HttpResponseRedirect("listing/" + new_listing_id)
    else:
        raise ValueError


@login_required(login_url="/login")
def bid(request, id):
    if request.method == "GET":
        return bid_if_GET(request, id)

    elif request.method == "POST":
        return bid_if_POST(request, id)

    else:
        return bid_if_GET(request)


def bid_if_GET(request, id):
    form = bid_form()
    return render(request, "auctions/bid.html", {"form": form,
                                                 "id": id})


@login_required(login_url="/login")
def bid_if_POST(request, id):
    form = bid_form(request.POST)

    if form.is_valid():
        item_listing = Listing.objects.get(id=id)
        bidder = request.user
        new_bid_amount = Decimal(form.cleaned_data['amount'])

        if is_bid_valid(item_listing, new_bid_amount):
            new_bid = Bid()
            new_bid.amount = new_bid_amount
            new_bid.bidder = bidder
            new_bid.item = item_listing
            new_bid.save()
            return HttpResponseRedirect("/listing/"+id)
        else:

            return HttpResponseRedirect("/listing/"+id, {"message": messages.warning(request, 'Invalid Bid!')})

    return HttpResponseRedirect("listing/"+id, {"message": messages.warning(request, 'Invalid Form!')})


def is_bid_valid(item_listing, new_bid_amount):
    current_bid_amount = item_listing.get_current_bid()
    starting_bid = item_listing.starting_bid
    if new_bid_amount > (current_bid_amount + Decimal(0.99)) and new_bid_amount >= starting_bid:
        return True
    return False


@ login_required(login_url="/login")
def add_listing(request):
    if request.method == "GET":
        return render(request, "auctions/add_listing.html")

    elif request.method == "POST":
        # process listing
        return

    else:
        raise Exception()


def category_view(request, category):
    listings = Listing.objects.get(category=category)
    return main_view(request, listings)
