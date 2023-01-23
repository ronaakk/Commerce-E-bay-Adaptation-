from django import forms
from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, FileInput
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

# Creating a listing form out of the Listings model
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['creator', 'bid_counter', 'active', 'winner']
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control', "style": "margin-bottom: 10px"}),
            'description': Textarea(
                attrs={'rows': 10, 'columns':4, 'class': 'form-control', "style": "margin-bottom: 10px"}),
            'minimum_bid' : NumberInput(
                attrs={"class": "form-control", "style": "margin-bottom: 10px"}),
            'starting_bid': NumberInput(attrs={'class': 'form-control'}),
            'category' : Select(attrs={'choices': Listing.CATEGORIES, "class": "form-control"}),
            'image' : FileInput(attrs={'class':'form-control', 'required': False})
        }

# Creating a bid form
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

    widgets = {
            'bid' : NumberInput(
                attrs={"class": "form-control", "style": "margin-bottom: 10px"}),
        }

