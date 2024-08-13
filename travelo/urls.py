from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("destinations/", views.get_destination),
    path("package/", views.create_package),
    path("destination/<int:id>", views.destination_details, name = "destination_details"),
]