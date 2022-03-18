from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

# category_choices = (
#     ('default', '...')
#     ('electronics', 'Electronics'),
#     ('home', 'Home'),
#     ('toys', "Toys"),
#     ('fashion', "Fashion")
# )


# MODELS
class User(AbstractUser):
    pass


# Auction Listings
class ListingItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    starting_bid = models.FloatField()

    img_url = models.URLField()  # models.ImageField()
    # category = models.CharField(choices=category_choices, default=default)

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
        fields = ['title', 'description', 'starting_bid', 'img_url']