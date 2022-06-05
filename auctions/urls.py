from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like_view/<int:listing_id>",views.like_view, name = "like" ),
    path("unlike_view/<int:listing_id>",views.unlike_view, name = "unlike" ),
    path("page_view/<int:listing_id>", views.page_view, name = "page" ),
    path("addlisting",views.addListing_view, name="addlisting"),
    path("addcomment_view/<int:listing_id>", views.addComment_view, name= "comment"),
    path("watchlist",views.watchlist, name = "watchlist"),
    path("profile", views.profileView,name= "profile"),
    path("deleteListing/<int:listingID>",views.deleteListing_view, name="deleteListing"),
    path("placeBidView/<int:listingID>", views.placeBidView, name= "placeBid"),
    path("buy/<int:listingID>", views.buy, name = "buy"),
    path("deleteComment_view/<int:listingID>/<int:commentID>", views.deleteComment_view, name= "dcomment")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                                document_root=settings.MEDIA_ROOT)