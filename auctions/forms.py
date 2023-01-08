from django import forms

from .models import *


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

# Creating a new listing form
class NewListingForm(forms.Form):
    title = forms.CharField(label='', min_length=2, widget=forms.TextInput(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Title"}))
    description = forms.CharField(label='', widget=forms.Textarea(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Description"}))
    price = forms.DecimalField(label='', widget=forms.NumberInput(
        attrs={"class": "form-control", "style": "margin-bottom: 10px", "placeholder": "Starting Bid ($)"}))
    image = forms.ImageField(label="Choose an Image for your Listing")
    category = forms.MultipleChoiceField(
        label='Pick a Category', widget=forms.CheckboxSelectMultiple, choices=Listing.CATEGORIES)
