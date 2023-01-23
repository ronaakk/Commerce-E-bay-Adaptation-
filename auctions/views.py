from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


def index(request):
    try:
        active_listings = Listing.objects.filter(active=True)
    except:
        active_listings = None

    # If someone is logged in
    user = request.user
    if user.id != None:
        try:
            watchlist = PersonalWatchList.objects.get(user=request.user)
            watchlist_listings = watchlist.listings.all()
        except:
            watchlist = None
            watchlist_listings = None
        
        return render(request, "auctions/index.html", {
            "active_listings": active_listings,
            "watchlist": watchlist,
            "watchlist_listings": watchlist_listings
        })
    else:
        return render(request, "auctions/index.html", {
            "active_listings": active_listings
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        # Returns a user object
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == "POST":
        # Passing in the form that was submitted
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]

            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "auctions/register.html", {
                    "message": "Passwords must match.",
                    "register_form": form
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "auctions/register.html", {
                    "message": "Username already taken.",
                    "register_form": form
                })
            login(request, user)
            return redirect('index')
    else:
        return render(request, "auctions/register.html", {
            "register_form": RegisterForm()
        })


def createListing(request):
    creator = request.user
    if request.method == "POST":
        listing = ListingForm(request.POST, request.FILES)
        if listing.is_valid():
            
            minimum_bid = listing.cleaned_data['minimum_bid']
            starting_bid = listing.cleaned_data['starting_bid']
            title = listing.cleaned_data['title']
            description = listing.cleaned_data['description']
            category = listing.cleaned_data['category']
            image = request.FILES.get('image')

            if starting_bid > minimum_bid:
                messages.error(request, 'Starting bid cannot be higher than the Minimum bid.')
                return render(request, "auctions/create.html", {
                    "create_form": listing
                })

            # Using .objects.create much simpler solution
            auction = Listing.objects.create(
                creator=creator,
                title=title,
                description=description,
                minimum_bid=minimum_bid,
                starting_bid=starting_bid,
                category=category,
                image=image,
            )
            
            messages.success(request, "Listing Created Successfully.")
            return redirect(reverse('index'))

        else:
            messages.error(request, 'Image extension not available! Acceptable formats in jpeg, png, jpg.')
            return render(request, "auctions/create.html", {
                    "create_form": listing
                })
    else:
        return render(request, "auctions/create.html", {
            "create_form": ListingForm()
        })


def view(request, listing_title):
    listing = Listing.objects.get(title=listing_title)

    # If someone is logged in
    user = request.user
    if user.id != None:
        try:
            watchlist = PersonalWatchList.objects.get(user=request.user)
            watchlist_listings = watchlist.listings.all()
        except:
            watchlist = None
            watchlist_listings = None
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist,
            "watchlist_listings": watchlist_listings
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing
        })

@login_required(login_url='/login', redirect_field_name='add_to_watchlist')
def add_to_watchlist(request, listing_id):
    user = request.user

    # Retrieving the user watchlist (if it exists)
    try:
        watchlist_exists = PersonalWatchList.objects.get(user=request.user)
    except:
        watchlist_exists = None

    # If there isn't one for this user, make one
    if watchlist_exists == None:
        PersonalWatchList.objects.create(user=user)

    # Access that watchlist
    watchlist = PersonalWatchList.objects.get(user=user)

    # Getting the listing that was clicked
    listing = Listing.objects.get(id=listing_id)

    # Comparing the listings already present in their watchlist to the one that was hit
    if (listing not in watchlist.listings.all()):
        watchlist.listings.add(listing)
        watchlist.save()
    else:
        messages.error(request, "Listing is already in your Watchlist.")
        return redirect(reverse('index'))

    messages.success(request, f"'{listing}' added to your Watchlist.")
    return redirect(reverse('index'))

def watchlist(request):

    watchlist = PersonalWatchList.objects.get(user=request.user)
    listings = watchlist.listings.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })

def remove_from_watchlist(request, listing_id):

    watchlist = PersonalWatchList.objects.get(user=request.user)
    listing_to_remove = watchlist.listings.get(id=listing_id)
    watchlist.listings.remove(listing_to_remove)

    messages.success(request, f"'{listing_to_remove}' removed from your Watchlist.")
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listings.all()
    })

@login_required(login_url='/login', redirect_field_name='make_a_bid')
def make_a_bid(request, listing_id):

    listing = Listing.objects.get(id=listing_id)
    user = request.user

    if request.method == "POST":

        bidform = BidForm(request.POST)
        bids = Bid.objects.filter(auction=listing_id).order_by('-bid')
        bid = int(request.POST['bid'])
        
        if bids:
            current_price = int(bids[0].bid)
        else:
            current_price = int(listing.starting_bid)

        if bid > current_price:

            # Updating the listing data
            new_bid = Bid.objects.create(user=user, bid=request.POST['bid'], auction=listing, date_created=date.today())

            listing.bid_counter += 1
            listing.last_bid = new_bid
            listing.save()
        
            messages.success(request, f"Your bid of ${bid} was made successfully.")
            return render(request, "auctions/listing.html", {
                "listing": listing
            })
        else:
            messages.error(request, "Please try again.")
            return render(request, "auctions/bid.html", {
                "bid_form": bidform,
                "listing": listing
            })
    else:
        return render(request, "auctions/bid.html", {
            "bid_form": BidForm(),
            "listing": listing
        })
