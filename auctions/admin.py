from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, ListingItem, WatchList, Bid, ListingComment

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ListingItem)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(ListingComment)
