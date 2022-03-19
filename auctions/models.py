from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.db import models
from django.forms import ModelForm


from datetime import datetime as dt


# MODELS
class User(AbstractUser):
    pass


category_choices = [
    ('Electronics', 'Electronics'),
    ('Home', 'Home'),
    ('Toys', "Toys"),
    ('Fashion', "Fashion")
]


# Auction Listings
class ListingItem(models.Model):
    # Form
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    starting_bid = models.FloatField()
    img_url = models.URLField(blank=True)  # models.ImageField()
    category = models.CharField(max_length=50, choices=category_choices)

    # Auto-generated when submitted
    starting_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # ForeigKey to User.

    # Variable keeps track of current highest bid
    # highest_bid = models.FloatField()

    def __str__(self):
        return f"{self.title}"


# TODO - Bids
# class Bid(models.Model):
#     bid = models.FloatField()
#     author = models.ForeignKey(
#         'User',
#         on_delete=models.CASCADE,
#     ) # ForeigKey to User
#     date = models.DateTimeField()


# Comments on auction listings
# class ListingComment(models.Model):
#     comment = models.CharField()
#     author = models.CharField()  # ForeigKey to User
#     date = models.


class WatchList(models.Model):
    # id - autogenerated
    # user_id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # ForeigKey to User

    # item_id
    item = models.ForeignKey(
        ListingItem,
        on_delete=models.CASCADE,
    )  # ForeigKey to ListingItem

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.item}"
        # return f"User ID: {self.user}, Item ID: {self.item}"


# FORMS
class AddListingItemForm(ModelForm):
    class Meta:
        model = ListingItem
        fields = [  # fields = '__all__'
            'title',
            'description',
            'starting_bid',
            'img_url',
            'category'
        ]

        labels = {
            # Name of field : label Text
            'title': 'Title',
            'description': 'Description',
            'starting_bid': 'Starting Bid',
            'img_url': 'Image URL',
            'category': 'Category'
        }


# class AddWatchListForm(ModelForm):
#     class Meta:
#         model = WatchList
#         fields = '__all__'
