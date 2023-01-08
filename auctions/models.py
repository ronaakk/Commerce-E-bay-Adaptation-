from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

class Listing(models.Model):
    
    CATEGORIES = [
    ('Toys', 'Toys'),
    ('Electronics', 'Electronics'),
    ('Lifsetyle', 'Lifestyle'),
    ('Home', 'Home'),
    ('Fashion', 'Fashion')
    ]   

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.CharField(blank=True, max_length=1064)
    category = models.CharField(max_length=64, blank=True, choices=CATEGORIES)
    image = models.URLField(default='https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bid_counter = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, blank=True, null=True)

    def _str__(self):
        return f"{self.title} by {self.creator}"

class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    date_created = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid} made by {self.user}"
