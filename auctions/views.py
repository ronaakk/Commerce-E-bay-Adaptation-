from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request, "auctions/index.html")


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


# Making a register form
class RegisterForm(forms.Form):
    username = forms.CharField(label='', min_length=2, widget=forms.TextInput(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Username"}))
    email = forms.CharField(label='', min_length=5, widget=forms.TextInput(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Email"}))
    password = forms.CharField(label='', min_length=2, widget=forms.TextInput(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Password"}))
    confirmation = forms.CharField(label='', min_length=2, widget=forms.TextInput(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Confirm Password"}))


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
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "register_form": RegisterForm()
        })
