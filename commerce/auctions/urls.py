from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:id>", views.show_listing, name="show_listing"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/watchlist", views.add_watchlist, name="add_watchlist"),
    path("listing/<int:id>/close", views.close, name="close"),
    path("listing/<int:id>/comment", views.comment, name="comment"),
    path("wathclist", views.watchlist, name="watchlist"),
    path("new", views.new_listing, name="new_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
