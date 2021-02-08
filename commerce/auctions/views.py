from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid
from .forms import ListingForm, BidForm, CommentForm

@login_required
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            listing.watchers.add(request.user)
            return HttpResponseRedirect(reverse("index"))
        else: 
            context = { "form": form }
            return render(request, "auctions/new.html", context)
    else:
        context = { "form": ListingForm() }
        return render(request, "auctions/new.html", context)


def show_listing(request, id):
    listing = Listing.objects.get(pk=id)
    bids = Bid.objects.filter(listing=listing)
    bid_count = len(bids)
    if bid_count > 0:
        highest_bid = bids.order_by("value").last()
        highest_bidder = highest_bid.user
        highest_bid_value = highest_bid.value
    else:
        highest_bidder = None
        highest_bid_value = listing.starting_bid
    context = {
        "listing": listing,
        "bid_count": bid_count,
        "highest_bidder": highest_bidder,
        "highest_bid_value": highest_bid_value
    }
    return render(request, "auctions/listing.html", context)


@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchers=request.user)
    context = { "listings": listings }
    return render(request, "auctions/watchlist.html", context)


@login_required
def add_watchlist(request, id):
    listing = Listing.objects.get(pk=id)

    if listing not in request.user.watchlist.all():
        request.user.watchlist.add(listing)
    else:
        request.user.watchlist.remove(listing)

    return HttpResponseRedirect(reverse("show_listing", args=[id]))


@login_required
def bid(request, id):
    form = BidForm(request.POST)
    listing = Listing.objects.get(pk=id)

    if form.is_valid() and listing.active:
        bid = form.save(commit=False)
        bids = Bid.objects.filter(listing=listing)
        highest_bid = bids.order_by("value").last()

        if not highest_bid or bid.value > highest_bid.value:
            bid.user = request.user
            bid.listing = listing
            bid.save()

    return HttpResponseRedirect(reverse("show_listing", args=[id]))


@login_required
def close(request, id):
    listing = Listing.objects.get(pk=id)

    if listing.owner == request.user:
        listing.active = False
        listing.save()
    
    return HttpResponseRedirect(reverse("show_listing", args=[id]))


@login_required
def comment(request, id):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.listing = Listing.objects.get(pk=id)
        comment.user = request.user
        comment.save()
    
    return HttpResponseRedirect(reverse("show_listing", args=[id]))


def index(request):
    category = request.GET.get("category")

    listings = Listing.objects.filter(active=True)

    if category:
        listings = listings.filter(categories=category)

    context = { "listings": listings, "category": category }
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
