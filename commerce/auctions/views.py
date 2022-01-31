from asyncio import exceptions
from cmd import IDENTCHARS
from email import message
import mailbox
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
        "listings": listings,
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


def is_user_also_auctioneer(user, auctioneer):
    return str(user) == str(auctioneer)


def is_user_also_highest_bidder(user, bid):
    return user == bid.bidder


def show_listing(request, id):
    if request.method == "GET":
        return show_listing_GET(request, id)
    elif request.method == "POST":
        return show_listing_POST(request, id)
    else:
        return show_listing_GET(request, id)


def show_listing_GET(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)
    current_listing_category = current_listing.category

    is_highest_bidder = False

    if current_listing.number_of_bids > 0:
        current_bid = current_listing.get_current_bid()
        current_bid_amount = current_bid.amount
        is_highest_bidder = is_user_also_highest_bidder(
            request.user, current_bid)
    else:
        # No bids!!
        current_bid_amount = Decimal(0.00)

    is_auctioneer = is_user_also_auctioneer(
        request.user, current_listing.auctioneer)

    return render(request, "auctions/listing.html", {"listing": current_listing,
                                                     "current_bid_amount": current_bid_amount,
                                                     "categories": Listing.CATEGORIES,
                                                     "current_listing_category": current_listing_category,
                                                     "is_highest_bidder": is_highest_bidder,
                                                     "is_auctioneer": is_auctioneer})


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


@login_required(login_url="/login")
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
            item_listing.increment_bid_number()
            return HttpResponseRedirect("/listing/"+id)
        else:

            return HttpResponseRedirect("/listing/"+id, {"message": messages.warning(request, 'Invalid Bid!', extra_tags="alert alert-warning")})

    return HttpResponseRedirect("listing/"+id, {"message": messages.warning(request, 'Invalid Form!', extra_tags="alert alert-danger")})


def is_bid_valid(item_listing, new_bid_amount):
    current_bid_amount = item_listing.get_current_bid()
    starting_bid = item_listing.starting_bid
    if new_bid_amount > (current_bid_amount + Decimal(0.99)) and new_bid_amount >= starting_bid:
        return True
    return False


def category_view(request, category):
    listings = Listing.objects.filter(category=category)
    if len(listings) > 0:
        return main_view(request, listings)
    else:

        return HttpResponseRedirect(reverse("index"),
                                    {"message": messages.info(request, 'Sorry, your search resulted 0 Items!',
                                                              extra_tags="alert alert-primary")})


def inform_winner(user, listing):
    # Todo
    print("Todo")


def end_listing(listing_id):
    listing = Listing.objects.get(id=id)
    listing.open = False

    winning_bid = listing.get_current_bid()
    user = winning_bid.bidder

    inform_winner(user, listing)


def get_watchlist(user):
    watchlist = Watchlist.objects.filter(watcher=user)
    return watchlist


@login_required
def watchlist(request):
    user = request.user

    watched_items = get_watchlist(user)
    print(watched_items)
    if len(watched_items) > 0:
        return main_view(request, watched_items)
    else:
        return HttpResponseRedirect(reverse("index"),
                                    {"message": messages.info(request, 'You PROBABLY have no items on your watchlist!',
                                                              extra_tags="alert alert-primary")})


@login_required
def toggle_watchlist(request, id):
    if request.method == "POST":
        print(id)
        listing = Listing.objects.get(id=id)
        print(f"listing:{listing}")
        user = request.user
        print(f"user:{user}")
        watched_items = get_watchlist(user)
        print(watched_items)
        if listing not in watched_items():
            new_watchlist_item = Watchlist()
            new_watchlist_item.watcher = user
            new_watchlist_item.watched_item = listing
            print(new_watchlist_item)
            new_watchlist_item.save()

        else:
            # remove from watchlist
            watchlist_item = get_model(
                watched_item == listing, watcher == user)
            watched_item.delete()
            print("none")
    return HttpResponseRedirect(reverse('watchlist'))
