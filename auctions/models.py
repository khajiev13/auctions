from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(blank=True, unique=True)

    def __str__(self):
        return f"{self.get_full_name()}"


class Category(models.Model):
    tag_value = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return f"{self.tag_value}"


class Listing(models.Model):
    # Who posted the listing auction
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    price = models.IntegerField(max_length=15)

    title = models.CharField(max_length=255)
    description = models.TextField(
        max_length=500, default="Description Not Provided")
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    category_id = models.ManyToManyField(
        Category, related_name="category_listings", blank=True, null=True)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bits_made")
    timestamp = models.DateTimeField(auto_now_add=True)
    cost_value = models.IntegerField(blank=False)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user_id.first_name} offered {self.cost_value}"


class Comment(models.Model):
    # Which listing the comment belongs
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    # Who left the comment: Store user's ID
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.user_id.first_name}'s comment"
