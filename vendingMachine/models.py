from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()

class Block(models.Model):
    code_id = models.IntegerField()
    item_id = models.IntegerField()
