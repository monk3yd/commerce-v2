from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, ListingItem, AddListingItemForm, WatchList, BidForm
# from .forms import AddListingItemForm

from datetime import datetime as dt


def index(request):
    # - Query database for all listings
    listings = ListingItem.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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


@login_required
def create(request):
    if request.method == "POST":
        form = AddListingItemForm(request.POST)
        if form.is_valid():
            # - Add new Listing to database
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            img_url = form.cleaned_data['img_url']
            category = form.cleaned_data['category']

            # Get datetime of listing
            now = dt.now()

            # Get id of user who make request
            # Get user object by id
            user = User.objects.get(pk=request.user.id)

            # Create new Listing Item
            item = ListingItem(
                title=title,
                description=description,
                starting_bid=starting_bid,
                img_url=img_url,
                category=category,
                starting_date=now,
                author=user
            )
            # Save new Listing Item
            item.save()
            return HttpResponseRedirect(reverse("index"))

    # Create form object and pass it to html
    form = AddListingItemForm()

    return render(request, "auctions/create.html", {
        "form": form
    })


def item(request, item_uid):
    # - Get Item
    item = ListingItem.objects.get(id=item_uid)
    # print(item.description)  # object access with .

    # Get form
    form = BidForm()

    # Add Item to Watchlist
    if request.method == "POST":
        # Get user id and User object
        user = User.objects.get(pk=request.user.id)

        try:
            # Create & Save item to users watchlist
            watch_item = WatchList(user=user, item=item)
            watch_item.save()
            item.in_watchlist = True
            item.save()
        except IntegrityError:
            return HttpResponseRedirect(reverse('watchlist'))

        return HttpResponseRedirect(reverse('watchlist'))

    # try:
        # # Get user
        # user = User.objects.get(pk=request.user.id)

        # # Get users watchlist
        # watchlist = WatchList.objects.filter(user=user, item=item)

        # # Check every item in watchlist if matches actual item
        # for _ in watchlist:
        #     if _.item == item:  # If they are the same means items already exists in watchlist
        #         item.in_watchlist = True
        #         break
        #     item.in_watchlist = False
        # print(item.in_watchlist)

    return render(request, "auctions/item.html", {
        "item": item,
        "in_watchlist": item.in_watchlist,
        "form": form
        })
    # No User or No Watchlist
    # except ObjectDoesNotExist:
    #     return render(request, "auctions/item.html", {
    #         "item": item,
    #         "form": form
    #     })

@login_required
# Render each user's watchlist
def watchlist(request):
    # Get user
    user = User.objects.get(pk=request.user.id)
    # Get all watchlist items that belongs to actual user
    watchlist = WatchList.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


# Remove item from watchlist
@login_required
def remove(request, item_uid):
    user = User.objects.get(pk=request.user.id)
    item = ListingItem.objects.get(id=item_uid)
    WatchList.objects.filter(user=user, item=item).delete()
    item.in_watchlist = False
    item.save()
    return HttpResponseRedirect(reverse("watchlist"))


# Close active listing item
@login_required
def close(request, item_uid):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        item = ListingItem.objects.get(author=user, id=item_uid)
        item.is_active = False
        item.save()

    return HttpResponseRedirect(reverse('item', args=(item_uid,)))


#  TODO - Only for login user (use decorator?)
@login_required
def bid(request, item_uid):
    form = BidForm(request.POST)
    if form.is_valid():
        # Get item
        bid = form.cleaned_data['bid']
        # Get bidded item
        item = ListingItem.objects.get(id=item_uid)
        # Get actual user
        user = User.objects.get(pk=request.user.id)

        # Validate : at least as large as the starting bid
        # Validate : greater than any other bids that have been placed.
        if item.starting_bid <= bid and item.highest_bid < bid:
            # print(True)
            # Replace highscore bid and save it to the database
            item.highest_bid = bid
            item.highest_bid_user = user.username
            item.save()
            return HttpResponseRedirect(reverse('item', args=(item_uid,)))

        print(item.in_watchlist)
        form = BidForm()
        return render(request, "auctions/item.html", {
            "item": item,
            "form": form,
            "in_watchlist": item.in_watchlist,
            "message": "Your bid is too low!"
        })

    # form = BidForm()
    # return render(request, "auctions/item.html", {
    #         "item": item,
    #         "form": form
    #     })