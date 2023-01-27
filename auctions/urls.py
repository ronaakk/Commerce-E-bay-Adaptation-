from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("view/<str:listing_title>", views.view, name="view"),
    path("addtowatchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("make_a_bid/<int:listing_id>", views.make_a_bid, name="make_a_bid"),
    path("close/<int:listing_id>", views.close_listing, name="close"),
    path("closed", views.closed_listings_page, name="closed_listings_page"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("delete_comment/<str:listing_title>/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("categories", views.categories, name="categories")
]
