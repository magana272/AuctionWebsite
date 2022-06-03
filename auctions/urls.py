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
    path("watchlist",views.watchlist, name = "watchlist")
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)