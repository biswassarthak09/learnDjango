from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ItemSerializer, BlockSerializer, BlockContainer, BuySuccessResponse
from .models import Item, Block
from django.db.models import Q


# Create your views here.
def open_vending_machine(request):
    blocks = Block.objects.all()
    block_content = []
    for block in blocks:
        # item = Item.objects.get(id=block.item_id)
        item = Item.objects.filter(
                    Q(id=block.item_id) & Q(quantity__gt=0)
                ).exclude(quantity=0).first()
        if item is not None:
            block_content.append(BlockContainer(item.name, item.price, block.code_id))
    return render(request, "vending.html", {'blocks': block_content})


#rest apis
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_item_by_id(request):
    item_id = request.data.get('id')
    item = Item.objects.filter(id=item_id)
    serializer = ItemSerializer(item, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_block_by_id(request):
    block_id = request.data.get('id')
    block = Block.objects.filter(id=block_id)
    serializer = ItemSerializer(block)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_blocks(request):
    blocks = Block.objects.all()
    serializer = BlockSerializer(blocks, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    try:
        if serializer.is_valid():
            # Save the Destination instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_block(request):
    item_id = request.data.get('item_id')
    if item_id is not None:
        try:
            item_exists = Item.objects.filter(id=item_id).exists()
            if not item_exists:
                return Response({'detail': 'Item with the provided ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = BlockSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Item.DoesNotExist:
            return Response({'detail': 'Error creating package'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def select_item(request):
    item_code = int(request.data.get('item_code'))
    try:
        block = Block.objects.filter(code_id=item_code).get()
        
        if block is None:
            return Response({'detail': 'Item with the provided code does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        item = Item.objects.filter(
                Q(id=block.item_id) & Q(quantity__gt=0)
            ).get()
        if item is None:
            return Response({'detail': 'Item with the provided code does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ItemSerializer(item)
        return Response({'item' : serializer.data}, status=status.HTTP_200_OK)

    except Item.DoesNotExist:
        return Response({'detail': 'Error creating item'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
def buy_item(request):
    item_id = int(request.data.get('item_id'))
    coins = float(request.data.get('coins'))
    item = Item.objects.get(id=item_id)
    if item is None:
        return Response({'detail': 'Item with the provided code does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if coins < item.price:
        return Response({'detail': 'Not enough money.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if coins >= item.price:
        change = coins - item.price
        item.quantity -= 1
        item.save()
        success_response = BuySuccessResponse(item.name, change);

        response_data = {
            'item_name': success_response.item_name,
            'change': success_response.change,
        }

        return Response({'response': response_data}, status=status.HTTP_200_OK)

        

