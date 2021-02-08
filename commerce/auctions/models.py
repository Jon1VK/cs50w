from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    owner = models.ForeignKey(User, related_name="owned_listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=500)
    starting_bid = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return self.title


class Bid(models.Model):
    value = models.PositiveIntegerField()
    user = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.listing}: {self.value}'


class Comment(models.Model):
    content = models.TextField(max_length=500)
    user = models.ForeignKey(User, related_name="comments", null=True, on_delete=models.SET_NULL)
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.listing}: {self.content}'
    