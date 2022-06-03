import re
from unicodedata import name
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import auctions


from .models import Like, User, Bid, Listing, Comment


def index(request):
    images = map(lambda x: x.image, Listing.objects.all())
    cats = ["Hoodies", "Shirt", "Pant", "Hat", "Electronic"]
    try : 
        like_list = list(map(lambda x : x.post.id, Like.objects.filter(user = request.user)))
    except:
        like_list = []

    return render(request, "auctions/index.html", {"listings": Listing.objects.all(), "images":images, "userlikes":like_list, "cats" :cats}
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
@login_required
def like_view(request, listing_id):
    if request.method == "POST":
        listing_finder = Listing.objects.get(pk=listing_id)
        try : 
            like_exist = Like.objects.get(user = request.user, post = listing_finder)
        except:
            like_exist = None
        if like_exist is None:
            newlike = Like(post=listing_finder, user = request.user, liked = True)
            newlike.save()
            listing_finder.likes +=1
            listing_finder.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    return HttpResponseRedirect(reverse("auctions:index"))
@login_required
def unlike_view(request, listing_id):
    if request.method == "POST":
        listing_finder = Listing.objects.get(pk=listing_id)
        try : 
            like_exist = Like.objects.get(user = request.user, post = Listing.objects.get(pk=listing_id))
            print(like_exist)
        except:
            like_exist = None
        print(like_exist)
        if like_exist is not None:
            print("we made it here")
            listing_finder = Listing.objects.get(pk=listing_id)
            listing_finder.likes -=1
            listing_finder.save()
            like_exist.delete()
            return HttpResponseRedirect(reverse("auctions:index"))
    return HttpResponseRedirect(reverse("auctions:index"))
def page_view(request,listing_id):
    listing = Listing.objects.get(pk =listing_id)
    return render(request, "auctions/page.html", {"listing":listing})

def addListing_view(request):
    cats = ["Hoodies", "Shirt", "Pant", "Hat", "Electronic", "Boards"]
    if request.method  == "POST":
        new_ = Listing(itemName = request.POST["itemName"], catagory = request.POST["Catagory"], price = request.POST["cost"], image = request.POST["image"])
        new_.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/addlisting.html", {"cats": cats})
def addComment_view(request,listing_id):
    ...
def watchlist(request):
    return render(request, "auctions/watchlist.html")

