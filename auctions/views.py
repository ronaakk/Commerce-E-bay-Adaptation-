from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import *
from .models import User


def index(request):
    active_listings = Listing.objects.filter(active=True)

    if active_listings is None:
        return render(request, "auctions/index.html")

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
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

