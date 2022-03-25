from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:item_uid>", views.item, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove/<int:item_uid>", views.remove, name="remove"),
    path("close/<int:item_uid>", views.close, name="close"),
    path("bid/<int:item_uid>", views.bid, name="bid"),
    path("comment/<int:item_uid>", views.comment, name="comment"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category, name="category"),
]
