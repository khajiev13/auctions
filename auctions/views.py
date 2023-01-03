from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import requests

from .models import Listing, User, Bid, Comment, Category


# def load_data(request):
#     # This function is not required for the project. It's just for loading listings automatically from API so that I don't have to do them manually
#     categories = requests.get('https://fakestoreapi.com/products/categories/')
#     products = requests.get('https://fakestoreapi.com/products/')
#     # for category in categories.json():
#     #     new_category = Category.objects.create(tag_value=category)
#     #     new_category.save()
#     user = User.objects.get(pk=request.user.id)
#     for product in products.json():
#         new_listing = Listing.objects.create(
#             user_id=user, title=product['title'], price=product['price'], image_url=product['image'], description=product['description'])
#         new_listing.save()
#         new_listing.category_id.add(
#             Category.objects.get(tag_value=product['category']))

#     return HttpResponse(new_listing)


def index(request):
    # Check if there is a session called watchlist
    if "watchlist" not in request.session:
        # if doesn't exist then create one
        request.session['watchlist'] = []

    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


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


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_listing(request):
    # Check for POST request and redirect the user to the new created listing
    if request.method == "POST":
        new_category = request.POST.get('new_category', None)
        categories = Category.objects.filter(
            id__in=list(map(int, request.POST.getlist('categories'))))
        title = request.POST.get('title', None)
        price = request.POST.get('price', None)
        description = request.POST.get('description', None)
        image_url = request.POST.get('image_url', None)
        user = User.objects.get(pk=request.user.id)
        if len(categories) > 0:
            # If categories list is not empty then we can create the listing
            new_listing = Listing.objects.create(
                user_id=user, title=title, price=price, image_url=image_url, description=description)
            new_listing.save()
            new_listing.category_id.set(categories)
            HttpResponseRedirect(reverse("view_listing", kwargs={
                                 'listing_id': new_listing.id}))
        # Check if a new category has been added
        elif new_category is not None:
            new_category = Category.objects.create(tag_value=new_category)
            new_category.save()
    categories = Category.objects.all()
    return render(request, "auctions/add_listing.html", {
        "categories": categories
    })


def view_listing(request, listing_id):
    message = ""
    listing = Listing.objects.get(id=listing_id)
    # For a post request add a comment or bid
    if request.method == "POST":

        # Get the data from post request
        closed = int(request.POST.get('closed', 0))
        comment = request.POST.get('comment', None)
        bid = request.POST.get('new_bid', None)
        watchlist = request.POST.get('watchlist', None)
        listing = Listing.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        # Check if the listing has been added or removed from the watchlist
        if watchlist is not None:
            if int(watchlist) not in request.session['watchlist']:
                request.session['watchlist'] += [listing_id]
            else:
                request.session['watchlist'].remove(listing_id)
            request.session.modified = True

        # Check if the listing has been closed
        if bool(closed):
            if len(listing.bids.all()) > 0:
                listing.winner = listing.bids.all().last().user_id
                listing.active = False
                listing.save()
                message = f"This listing has been closed and the winner is {listing.winner}"
            else:
                message = "The listing doesn't have any bids offered!"
        # Check if comment or bid has been placed
        if comment is not None:
            if len(comment) == 0:
                message = "Empty comment!"
            else:
                new_comment = Comment.objects.create(
                    listing_id=listing, user_id=user, text=comment)
                new_comment.save()
                message = "The new comment has been posted succesfully"
        # Check if a bid has been placed
        if bid is not None:
            if len(bid) is not 0:
                bid = int(bid)
                try:
                    # Check if the new bid is higher than the last one
                    if bid > listing.price and (bid > listing.bids.all().last().cost_value and hasattr(listing.bids.all().last(), 'cost_value')):
                        new_bid = Bid.objects.create(
                            listing_id=listing, user_id=user, cost_value=bid)
                        new_bid.save()
                        message = "The new bid has been placed succesfully"
                    else:
                        message = "The new bid to be placed must be higher than the price or last bid"
                # If the listing has no previous bids and  raises an attribute error, we still wanna add the new bid
                except AttributeError:
                    new_bid = Bid.objects.create(
                        listing_id=listing, user_id=user, cost_value=bid)
                    new_bid.save()
                    message = "The new bid has been placed succesfully"
            else:
                message = "You placed an empty bid!"
                # Get the specific values and render them on the website
    categories = listing.category_id.all()
    bids = Bid.objects.filter(listing_id=listing_id)
    comments = listing.comments.all()
    watchlist = request.session['watchlist']
    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "categories": categories,
        "bids": bids,
        "comments": comments,
        "message": message,
        'watchlist': watchlist
    })


def categories(request):
    listings = None
    categories = Category.objects.all()
    if request.method == "POST":
        category_id = int(request.POST.get('category', "1"))
        category = Category.objects.get(pk=category_id)
        listings = category.category_listings.filter(active=True)
    return render(request, "auctions/categories.html", {
        "listings": listings,
        "categories": categories
    })


def watchlist(request):

    listings = Listing.objects.filter(
        pk__in=request.session['watchlist'], active=True)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
