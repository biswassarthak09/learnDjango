from django.urls import path
from . import views

urlpatterns = [
    path("", views.open_vending_machine, name = "open_vending_machine"),
    path("select_item/", views.select_item, name = "select_item"),
    path("buy_item/", views.buy_item, name = "buy_item"),

    path("api/get_items/", views.get_items, name = "get_items"),
    path("api/get_item/<int:id>", views.get_item_by_id, name = "get_item"),
    path("api/get_block/<int:id>", views.get_block_by_id, name = "get_block"),
    path("api/get_blocks/", views.get_blocks, name = "get_blocks"),
    path("api/create_item/", views.create_item, name = "create_item"),
    path("api/create_block/", views.create_block, name = "create_block"),
]