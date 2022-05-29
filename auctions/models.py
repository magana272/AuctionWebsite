from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/photos')
class User(AbstractUser):
    first  = models.CharField(max_length=50)
    last   = models.CharField(max_length=65)
    def __str__(self)->str:
        return f"{self.first} {self.last}"
class Listing(models.Model):
    itemName  = models.CharField(max_length=65)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    catagory  = models.CharField(max_length=50)
    price =  models.FloatField()
    description = models.TextField()
    image = models.ImageField()
    def __str__(self)-> str:
        return f"Item Nanme:{self.itemName}, Created By{self.poster}, Price: {self.price}"
class Bid(models.Model):
    listing = models.ForeignKey(Listing,on_delete = models.CASCADE)
    placedBy  = models.ForeignKey(User,on_delete=models.CASCADE)
    bidPrice =  models.IntegerField()
    def __str__(self) -> str:
        return f"{self.placedBy} bid {self.bidPrice} for {self.listing}"
class Comment(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    placeby = models.ForeignKey(User,on_delete=models.CASCADE)   
    comment = models.TextField()
    def __str__(self)->str:
        return f"{self.placeby} commeneted{self.comment} on {self.post}"





