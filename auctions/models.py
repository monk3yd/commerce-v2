from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


# MODELS
class User(AbstractUser):
    pass


category_choices = [
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('toys', "Toys"),
    ('fashion', "Fashion")
]


# Auction Listings
class ListingItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    starting_bid = models.FloatField()

    img_url = models.URLField()  # models.ImageField()
    category = models.CharField(max_length=50, choices=category_choices)

    def __str__(self):
        return f"List Item: {self.title}"


# Bids
# class Bid(model.Models):
#     bid =
#     author = 
#     date =


# Comments on auction listings
# class ListingComment(models.Model):
#     comment = models.CharField()
#     author = models.CharField()  # ForeigKey to User
#     date = models.

# FORMS
class AddListingItemForm(ModelForm):
    class Meta:
        model = ListingItem
        fields = ['title', 'description', 'starting_bid', 'img_url', 'category']  # fields = '__all__'
        labels = {
            # Name of field : label Text
            'title': 'Title',
            'description': 'Description',
            'starting_bid': 'Starting Bid',
            'img_url': 'Image URL',
            'category': 'Category'
        }
        # field_classes = {
        #     'title': 
        # }
