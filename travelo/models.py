from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price =  models.IntegerField()
    rating = models.IntegerField()
    reviews = models.IntegerField()
    days = models.IntegerField()


class Package(models.Model):
    destination_id = models.IntegerField()
    description = models.TextField()
    day_wise = models.JSONField()

        