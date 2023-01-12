from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import *
from .models import User


def index(request):
    return render(request, "auctions/index.html")


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
    if request.method == "POST":

        minimum_bid = request.POST['minimum_bid']
        starting_bid = request.POST['starting_bid']

        if starting_bid > minimum_bid:
            messages.error(request, 'Starting bid cannot be higher than the Minimum bid.')
            return render(request, "auctions/create.html", {
                "create_form": ListingForm(request.POST)
            })
    
        creator = request.user
        title = request.POST['title']
        description = request.POST['description']
        image = request.POST['image']
        category = request.POST['category']

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

        return render(request, "auctions/index.html", {
            "message": "Listing Created Successfully."
        })
    else:
        return render(request, "auctions/create.html", {
            "create_form": ListingForm()
        })
