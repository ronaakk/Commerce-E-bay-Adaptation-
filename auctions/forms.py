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
