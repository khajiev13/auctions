from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("load_data", views.load_data, name="load_data"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listings/<int:listing_id>", views.view_listing, name="view_listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist")
]
