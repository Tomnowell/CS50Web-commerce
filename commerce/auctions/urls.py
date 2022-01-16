from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_listings", views.show_entries, name="all_listings"),
    path("listing/<str:id>", views.show_listing, name="listing"),
    path("create", views.create, name="create")

]
