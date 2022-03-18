from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, ListingItem, AddListingItemForm, WatchList
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
            uid = request.user.id
            # Get user object by id
            user = User.objects.get(pk=uid)

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
    return render(request, "auctions/item.html", {
        "item": item
    })


def watchlist(request):
    if request.method == "POST":
        uid = request.user.id
        user = User.objects.get(pk=uid)
        item = ListingItem.objects.get(author=user)

        watch_item = WatchList(user=user, item=item)
        watch_item.save()
        return HttpResponseRedirect(reverse('watchlist'))
    # Get all watchlist items with that belongs to actual user
    watchlist = WatchList.objects.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


# Remove item from watchlist
def remove(request):
    uid = request.user.id
    print(uid)
    user = User.objects.get(pk=uid)
    print(user)
    item = ListingItem.objects.get(author=user)
    print(item)
    WatchList.objects.filter(item=item).delete()
    return HttpResponseRedirect(reverse("watchlist"))
