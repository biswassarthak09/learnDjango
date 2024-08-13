from rest_framework import serializers
from .models import Package, Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['name', 'desc', 'price', 'rating', 'reviews', 'days']


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['destination_id', 'description', 'day_wise']

