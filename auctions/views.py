
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import auctions
from .models import Like, User, Bid, Listing, Comment

cats = ["Hoodies", "Shirts", "Pants", "Hats", "Electronics", "Skateboards","Accessories", "Shoes"]
def index(request):
    images = map(lambda x: x.image, Listing.objects.all())
    cats = ["Hoodies", "Shirts", "Pants", "Hats", "Electronics", "Skateboards","Accessories", "Shoes"]
    try : 
        like_list = list(map(lambda x : x.post.id, Like.objects.filter(user = request.user)))
    except:
        like_list = []
    if request.method == "GET" and "cat" in request.GET:
        cat = request.GET["cat"]
        if cat == "All":
            return render(request, "auctions/index.html", {"listings": Listing.objects.all(), "images":images, "userlikes":like_list, "cats" :cats})
        return render(request, "auctions/index.html", {"listings": Listing.objects.filter(catagory = cat), "images":images, "userlikes":like_list, "cats" :cats})
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
            user = User.objects.create_user(username = username, email = email, password =password)
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
        except:
            like_exist = None
        if like_exist is not None:
            listing_finder = Listing.objects.get(pk=listing_id)
            listing_finder.likes -=1
            listing_finder.save()
            like_exist.delete()
            return HttpResponseRedirect(reverse("auctions:index"))
    return HttpResponseRedirect(reverse("auctions:index"))
def page_view(request,listing_id):
    listing = Listing.objects.get(pk =listing_id)
    try:
        highestbid = max(list(map(lambda x : x.bidPrice ,Bid.objects.filter(listing = listing))))
    except:
        highestbid = "No currentbids"   
    try: 
        comments = Comment.objects.filter(post=listing)
    except :
        comments = "No commentssss"        
    return render(request, "auctions/page.html", {"listing":listing, "highestbid":highestbid, "comments":comments})


def addListing_view(request):
    if request.method  == "POST":
        new_ = Listing(itemName = request.POST["itemName"], catagory = request.POST["Catagory"], price = request.POST["cost"], image = request.FILES["image"], description = request.POST["description"], poster = User.objects.get(pk=request.user.id))
        new_.save()
        return render(request, "auctions/addlisting.html",{"cats": cats})
    return render(request, "auctions/addlisting.html", {"cats": cats})
def deleteListing_view(request, listingID):
    if Listing.objects.get(pk=listingID):
        Listing.objects.get(pk=listingID).delete()
    return HttpResponseRedirect(reverse("auctions:profile"))
def addComment_view(request,listing_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            currentuser = request.user
            listing  =  Listing.objects.get(pk = listing_id )
            comment = request.POST["comment"]
            Comment(post = listing ,placeby = currentuser, comment = comment).save()
            return HttpResponseRedirect(reverse("auctions:page", kwargs={'listing_id':listing_id}))
    return HttpResponseRedirect(reverse("auctions:login"))
def watchlist(request):
    liked = Like.objects.filter(user = request.user)
    likedlistings = list(map(lambda x : x.post, liked))
    return render(request, "auctions/watchlist.html" , {"likedlistings":likedlistings})
def profileView(request):
    listings = Listing.objects.filter(poster= request.user)
    return render(request,"auctions/profile.html", {"listings":listings})

def placeBidView(request, listingID):
    if request.user.is_authenticated:
        bidValue = request.POST["bid"]
        if Listing.objects.get(pk=listingID):
                listing = Listing.objects.get(pk=listingID)
                placedBy  = User.objects.get(pk=request.user.id)
                Bid(listing = listing, placedBy=placedBy, bidPrice=bidValue).save()
        return HttpResponseRedirect(reverse("auctions:page", kwargs={'listing_id':listingID }))
    return HttpResponseRedirect(request, "auctions/index.html")
    
def buy(request,listingID):
    return render(request, "auctions/buy.html")

def deleteComment_view(request,listingID,commentID):
    
    Comment.objects.get(pk = commentID).delete()
    return HttpResponseRedirect(reverse("auctions:page", kwargs={'listing_id':listingID}))



