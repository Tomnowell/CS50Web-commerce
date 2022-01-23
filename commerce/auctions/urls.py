from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:id>", views.show_listing, name="listing"),
    path("listing/<str:id>/bid", views.bid, name="bid"),
    path("listing/<str:id>/end", views.end_listing, name="end_listing"),
    path("category/<str:category>", views.category_view, name="category"),
    path("create", views.create, name="create"),
    path("<str:user>/watchlist", views.watchlist, name="watchlist")
]
