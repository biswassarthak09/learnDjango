from django.shortcuts import render

from travelo.models import Destination, Package
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PackageSerializer, DestinationSerializer


# Create your views here.
def index(request):
    places = Destination.objects.all()
    return render(request, "index.html", {'places': places})

def destination_details(request, id):
    packages = Package.objects.filter(destination_id = id)
    destination = Destination.objects.get(id = id)
    return render(request, "destination_details.html", {'packages': packages, 'destination': destination})

#rest apis
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_destination(request):
    places = Destination.objects.all()
    serializer = DestinationSerializer(places, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_package(request):
    destination_id = request.data.get('destination_id')
    if destination_id is not None:
        try:
            # Check if the destination with the provided ID exists
            destination_exists = Destination.objects.filter(id=destination_id).exists()
            if not destination_exists:
                return Response({'detail': 'Destination with the provided ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # If the destination exists, create a Package instance
            # Create a serializer for the Package
            serializer = PackageSerializer(data=request.data)

            if serializer.is_valid():
                # Save the Destination instance
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Destination.DoesNotExist:
            return Response({'detail': 'Error creating package'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)