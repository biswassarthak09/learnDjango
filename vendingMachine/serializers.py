from rest_framework import serializers
from .models import Item, Block

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'quantity']


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['code_id', 'item_id']


class BlockContainer:
    def __init__(self, item_name, item_price, code_value):
        self.item_name = item_name
        self.item_price = item_price
        self.code_value = code_value

class BuySuccessResponse:
    def __init__(self, item_name, change):
        self.item_name = item_name
        self.change = change