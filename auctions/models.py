from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, FileInput
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

class Listing(models.Model):
    
    CATEGORIES = [
    ('Toys', 'Toys'),
    ('Electronics', 'Electronics'),
    ('Lifestyle', 'Lifestyle'),
    ('Home', 'Home'),
    ('Fashion', 'Fashion'),
    ('Other', 'Other')
    ]   

    # Validating image upload
    def validate_image(self):
        avaible_formats = [
            'png',
            'jpeg',
            'jpg',
            ]

        img = self.cleaned_data.get('image')
        
        if img:
            img_ext = img.name.split(".")[-1]
            if img.size > 4194304:
                raise ValidationError("Image size must be less than 4MB")
            if img_ext not in avaible_formats:
                raise ValidationError("Image extension is not avaible")        
        return img

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=64, blank=False, null=False)
    minimum_bid = models.IntegerField(blank=False, null=True) 
    description = models.CharField(blank=True, max_length=1064, null=True)
    starting_bid = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, choices=CATEGORIES)
    image = models.ImageField(
        default='https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png',
        upload_to='auctions/files/images',
        validators=[validate_image])
    bid_counter = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, blank=True, null=True)

    def _str__(self):
        return f"{self.title} by {self.creator}"

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

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid = models.IntegerField()
    date_created = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid} made by {self.user}"
