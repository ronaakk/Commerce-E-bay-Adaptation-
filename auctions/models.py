from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class User(AbstractUser):
    pass

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    item = models.ForeignKey('Listing', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"

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
    def validate_image(img):
        avaible_formats = [
            'png',
            'jpeg',
            'jpg',
            ]
        
        if img:
            img_ext = img.name.split(".")[-1]
            if img.size > 4194304:
                raise ValidationError("Image size must be less than 4MB")
            if img_ext not in avaible_formats:
                raise ValidationError("Image extension is not available")        
        return img

    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=35, blank=False, null=False)
    minimum_bid = models.IntegerField(blank=False, null=True) 
    description = models.CharField(blank=True, max_length=1064, null=True)
    starting_bid = models.IntegerField(blank=True, null=True)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, choices=CATEGORIES)
    image = models.ImageField(
        default='listing-images/default.jpeg',
        upload_to='auctions/files/images',
        validators=[validate_image])
    comments = models.ManyToManyField(Comment, blank=True)
    bid_counter = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.creator}"


class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_bid")
    bid = models.IntegerField()
    date_created = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey('Listing', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid} by {self.user}"


class PersonalWatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"Watchlist for {self.user}"