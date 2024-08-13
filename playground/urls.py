from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_hello, name = "say_hello"),
    path("add/", views.add_two_numbers, name = "add_two_numbers")
]

