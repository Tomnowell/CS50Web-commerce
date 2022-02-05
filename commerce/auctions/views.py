from asyncio import exceptions
from cmd import IDENTCHARS
from contextlib import nullcontext
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
    context = {"title": "Active Listings",
               "listings": listings}
    return main_view(request, context)


def main_view(request, context):
    context["categories"] = Listing.CATEGORIES
    return render(request, "auctions/index.html", context)


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


def get_comments(item_id):
    current_item = Listing.objects.get(id=item_id)
    all_comments = Comment.objects.filter(item=current_item)
    return all_comments


def set_listing_context(request, listing_id):

    current_listing = Listing.objects.get(id=listing_id)
    current_listing_category = current_listing.category

    empty_bid_form = bid_form()
    empty_comment_form = comment_form()

    is_auctioneer = is_user_also_auctioneer(
        request.user, current_listing.auctioneer)

    number_of_bids = current_listing.get_bid_count()
    if number_of_bids > 0:
        current_bid = current_listing.get_current_bid()
        current_bid_amount = current_bid.amount
        is_highest_bidder = is_user_also_highest_bidder(
            request.user, current_bid)
    else:
        # No bids!!
        current_bid_amount = "No bids!"

    try:
        all_comments = get_comments(listing_id)
    except (Comment.DoesNotExist):
        all_comments = "There are no comments for this item"

    context = {
        "listing": current_listing,
        "current_bid_amount": current_bid_amount,
        "categories": Listing.CATEGORIES,
        "current_listing_category": current_listing_category,
        "is_highest_bidder": is_highest_bidder,
        "is_auctioneer": is_auctioneer,
        "bid_form": empty_bid_form,
        "comment_form": empty_comment_form,
        "comments": all_comments
    }
    return context


def show_listing_GET(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)

    context = set_listing_context(request, listing_id)
    return render(request, "auctions/listing.html", context)


def show_listing_POST(request, listing_id):
    current_listing = Listing.objects.get(id=listing_id)
    comment = comment_form(request.POST or None)

    if comment.is_valid() and len(comment.cleaned_data['comment']) > 0:
        new_comment = Comment()
        new_comment.commentor = request.user
        new_comment.item = Listing.objects.get(id=listing_id)
        new_comment.comment = comment.cleaned_data['comment']
        new_comment.save()

    new_bid = bid_form(request.POST or None)
    if new_bid.is_valid:
        bid(request, listing_id)

    all_comments = get_comments(listing_id)
    context = set_listing_context(request, listing_id)

    return render(request, "auctions/listing.html", context)


def make_bid(user, bid_amount, listing_id):
    new_bid = Bid()
    new_bid.bidder = user
    new_bid.amount = bid_amount
    item_listing = Listing.objects.get(id=listing_id)
    new_bid.item = item_listing
    new_bid.save()
    item_listing.increment_bid_count()
    item_listing.save()


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


def is_bid_valid(item_listing, new_bid_amount):
    starting_bid = item_listing.starting_bid
    if item_listing.get_bid_count() > 0:
        current_bid = item_listing.get_current_bid()
        current_bid_amount = current_bid.amount
        if new_bid_amount > (current_bid_amount + Decimal(0.99)):
            return True
    elif new_bid_amount >= starting_bid:
        return True
    else:
        return False


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
    context = {
        "bid_form": bid_form(),
        "id": id
    }
    return render(request, "auctions/bid.html", context)


@login_required(login_url="/login")
def bid_if_POST(request, listing_id):
    form = bid_form(request.POST)
    user = request.user

    if form.is_valid():
        item_listing = Listing.objects.get(id=listing_id)
        bidder = request.user
        new_bid_amount = form.cleaned_data['amount']

        if is_bid_valid(item_listing, new_bid_amount):
            make_bid(bidder, new_bid_amount, listing_id)

            context = {
                "bid_form": bid_form()
            }
            return HttpResponseRedirect("/listing/"+listing_id, context)
        else:
            context = {
                "message": messages.warning(request, 'Invalid Bid!', extra_tags="alert alert-warning"),
                "bid_form": bid_form()
            }
            return HttpResponseRedirect("/listing/"+listing_id, context)

    context = {
        "message": messages.warning(request, 'Invalid Form!',
                                    extra_tags="alert alert-danger"),
        "bid_form": bid_form()
    }
    return HttpResponseRedirect("listing/"+listing_id,
                                context)


def category_view(request, category):
    listings = Listing.objects.filter(category=category)

    if len(listings) > 0:
        context = {
            "title": category,
            "listings": listings
        }
        return main_view(request, context)
    else:
        context = {
            "message": messages.info(request, 'Sorry, your search resulted 0 Items!',
                                     extra_tags="alert alert-primary")
        }
        return HttpResponseRedirect(reverse("index"), context)


def inform_winner(user, listing):
    # Todo
    print("Todo")


def end_listing(listing_id):
    listing = Listing.objects.get(id=id)
    listing.open = False

    winning_bid = listing.get_current_bid()
    user = winning_bid.bidder

    inform_winner(user, listing)


@ login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    print(listings)
    if len(listings) > 0:
        context = {
            "title": "Watchlist",
            "listings": listings
        }
        return main_view(request, context)
    else:
        context = {
            "message": messages.info(request, 'You have no items on your watchlist!',
                                     extra_tags="alert alert-primary")
        }
        return HttpResponseRedirect(reverse("index"), context)


@login_required
def toggle_watchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        print(f"Adding or removing listing{listing}")
        watchlist = request.user.watchlist
        all_watchlist = request.user.watchlist.all()
        print(f"all_watchlist {all_watchlist}")
        if listing in all_watchlist:
            print(f"Remove {listing} from {watchlist}")
            watchlist.remove(listing)
        else:
            print(f"Add {listing} to {watchlist}")
            watchlist.add(listing)
    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
